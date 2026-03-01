// sync.js — Client-side encrypted profile sync (AES-256-GCM)

import { exportAll, importAll } from '../db.js';
import { getAuthToken, isAuthenticated } from './identity.js';
import { createLogger } from './logger.js';

const log = createLogger('sync');

const API_URL = import.meta.env.VITE_API_URL || '';
const ENC_KEY_STORAGE = 'baseline_encryption_key';
const IV_LENGTH = 12;

// ---------------------------------------------------------------------------
// Encryption key management
// ---------------------------------------------------------------------------

let cachedKey = null;

/**
 * Get or create the AES-256-GCM encryption key.
 * Generated once, stored as base64 in localStorage.
 */
export async function getOrCreateEncryptionKey() {
  if (cachedKey) return cachedKey;

  const stored = localStorage.getItem(ENC_KEY_STORAGE);
  if (stored) {
    const raw = base64ToBytes(stored);
    cachedKey = await crypto.subtle.importKey('raw', raw, 'AES-GCM', true, ['encrypt', 'decrypt']);
    return cachedKey;
  }

  // Generate new 256-bit key
  cachedKey = await crypto.subtle.generateKey({ name: 'AES-GCM', length: 256 }, true, ['encrypt', 'decrypt']);
  const exported = await crypto.subtle.exportKey('raw', cachedKey);
  localStorage.setItem(ENC_KEY_STORAGE, bytesToBase64(new Uint8Array(exported)));
  return cachedKey;
}

export function hasEncryptionKey() {
  return localStorage.getItem(ENC_KEY_STORAGE) !== null;
}

/**
 * Export encryption key as base64 (for embedding in profile export).
 */
export function exportEncryptionKeyBase64() {
  return localStorage.getItem(ENC_KEY_STORAGE);
}

/**
 * Import encryption key from base64 (from profile import).
 */
export async function importEncryptionKey(base64) {
  localStorage.setItem(ENC_KEY_STORAGE, base64);
  cachedKey = null; // force re-import on next use
}

// ---------------------------------------------------------------------------
// Encrypt / Decrypt
// ---------------------------------------------------------------------------

async function encrypt(plaintext) {
  const key = await getOrCreateEncryptionKey();
  const iv = crypto.getRandomValues(new Uint8Array(IV_LENGTH));
  const encoded = new TextEncoder().encode(plaintext);
  const ciphertext = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, encoded);

  // Wire format: [12-byte IV][ciphertext+GCM tag] → base64
  const combined = new Uint8Array(IV_LENGTH + ciphertext.byteLength);
  combined.set(iv, 0);
  combined.set(new Uint8Array(ciphertext), IV_LENGTH);
  return bytesToBase64(combined);
}

async function decrypt(base64) {
  const key = await getOrCreateEncryptionKey();
  const combined = base64ToBytes(base64);
  const iv = combined.slice(0, IV_LENGTH);
  const ciphertext = combined.slice(IV_LENGTH);
  const decrypted = await crypto.subtle.decrypt({ name: 'AES-GCM', iv }, key, ciphertext);
  return new TextDecoder().decode(decrypted);
}

// ---------------------------------------------------------------------------
// Push / Pull
// ---------------------------------------------------------------------------

async function syncFetch(path, options = {}) {
  const token = getAuthToken();
  if (!token) throw new Error('Not authenticated');

  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...(options.headers || {}),
    },
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: res.statusText }));
    throw new Error(err.error || `HTTP ${res.status}`);
  }
  return res.json();
}

/**
 * Encrypt and push the full profile to the server.
 */
export async function pushProfile() {
  if (!isAuthenticated()) return;

  const data = await exportAll();
  const json = JSON.stringify(data);
  const encrypted = await encrypt(json);
  const updated_at = new Date().toISOString();

  await syncFetch('/sync/profile', {
    method: 'PUT',
    body: JSON.stringify({ encrypted, updated_at }),
  });

  log.info('profile pushed', { size: json.length });
}

/**
 * Pull and decrypt the profile from the server, replacing local data.
 */
export async function pullProfile() {
  if (!isAuthenticated()) return false;

  const result = await syncFetch('/sync/profile', { method: 'GET' });
  if (result.empty) return false;

  const json = await decrypt(result.encrypted);
  const data = JSON.parse(json);
  await importAll(data);
  log.info('profile pulled', { updated_at: result.updated_at });
  return true;
}

/**
 * Compare local vs remote timestamps and sync accordingly.
 * Returns 'pulled' | 'pushed' | 'noop'.
 */
export async function syncOnLogin() {
  if (!isAuthenticated()) return 'noop';
  if (!hasEncryptionKey()) {
    // No encryption key = first device, just push
    await pushProfile();
    return 'pushed';
  }

  try {
    const meta = await syncFetch('/sync/profile/meta', { method: 'GET' });
    if (meta.empty) {
      await pushProfile();
      return 'pushed';
    }

    const remoteTime = new Date(meta.updated_at).getTime();
    const data = await exportAll();
    const localTime = new Date(data.profile?.meta?.updated_at || 0).getTime();

    // Within 1 second = same, prefer local (no-op)
    if (Math.abs(remoteTime - localTime) < 1000) {
      return 'noop';
    }

    if (remoteTime > localTime) {
      const pulled = await pullProfile();
      if (pulled) {
        log.info('remote profile newer — pulled and reloading');
        window.location.reload();
        return 'pulled'; // won't reach here after reload
      }
    }

    // Local is newer — push
    await pushProfile();
    return 'pushed';
  } catch (err) {
    log.warn('sync failed', { error: err.message });
    return 'noop';
  }
}

// ---------------------------------------------------------------------------
// Debounced auto-push (fire-and-forget)
// ---------------------------------------------------------------------------

let pushTimer = null;

/**
 * Schedule a debounced push (5s). Collapses rapid writes into one push.
 * No-ops silently if not authenticated.
 */
export function schedulePush() {
  if (!isAuthenticated()) return;

  if (pushTimer) clearTimeout(pushTimer);
  pushTimer = setTimeout(() => {
    pushTimer = null;
    pushProfile().catch(err => {
      log.warn('auto-push failed', { error: err.message });
    });
  }, 5000);
}

// ---------------------------------------------------------------------------
// Base64 helpers
// ---------------------------------------------------------------------------

function bytesToBase64(bytes) {
  let binary = '';
  for (const byte of bytes) binary += String.fromCharCode(byte);
  return btoa(binary);
}

function base64ToBytes(str) {
  const binary = atob(str);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
  return bytes;
}
