// identity.js — Client-side passkey identity (WebAuthn + JWT)

import { startRegistration, startAuthentication } from '@simplewebauthn/browser';
import { createLogger } from './logger.js';

const log = createLogger('identity');

const API_URL = import.meta.env.VITE_API_URL || '';
const STORAGE_KEYS = {
  userId: 'baseline_user_id',
  token: 'baseline_auth_token',
};

// ── Feature detection ──

export function isPasskeySupported() {
  return typeof window.PublicKeyCredential !== 'undefined';
}

export async function isPlatformAuthenticatorAvailable() {
  if (!isPasskeySupported()) return false;
  try {
    return await PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable();
  } catch {
    return false;
  }
}

// ── User ID management ──

export function getUserId() {
  let id = localStorage.getItem(STORAGE_KEYS.userId);
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem(STORAGE_KEYS.userId, id);
  }
  return id;
}

// ── JWT management ──

function parseJWT(token) {
  try {
    const payload = token.split('.')[1];
    const padded = payload.replace(/-/g, '+').replace(/_/g, '/');
    return JSON.parse(atob(padded));
  } catch {
    return null;
  }
}

export function getAuthToken() {
  const token = localStorage.getItem(STORAGE_KEYS.token);
  if (!token) return null;
  const payload = parseJWT(token);
  if (!payload || !payload.exp) return null;
  // Check expiry with 60s buffer
  if (payload.exp < Date.now() / 1000 + 60) {
    localStorage.removeItem(STORAGE_KEYS.token);
    return null;
  }
  return token;
}

export function isAuthenticated() {
  return getAuthToken() !== null;
}

function storeAuth(token, userId) {
  localStorage.setItem(STORAGE_KEYS.token, token);
  localStorage.setItem(STORAGE_KEYS.userId, userId);
}

// ── API helpers ──

async function authFetch(path, body) {
  const res = await fetch(`${API_URL}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: res.statusText }));
    throw new Error(err.error || `HTTP ${res.status}`);
  }
  return res.json();
}

// ── Registration flow ──

export async function registerPasskey() {
  const userId = getUserId();
  log.info('starting passkey registration', { userId });

  // Step 1: Get registration options from server
  const { options, challengeId } = await authFetch('/auth/register/begin', { userId });

  // Step 2: Create credential via browser WebAuthn API
  const credential = await startRegistration({ optionsJSON: options });

  // Step 3: Verify with server, get JWT
  const result = await authFetch('/auth/register/complete', { challengeId, credential });

  if (result.verified && result.token) {
    storeAuth(result.token, result.userId);
    log.info('passkey registered successfully');
    return result;
  }

  throw new Error('Registration verification failed');
}

// ── Login flow ──

export async function loginWithPasskey() {
  log.info('starting passkey login');

  // Step 1: Get authentication options (discoverable — no userId needed)
  const { options, challengeId } = await authFetch('/auth/login/begin', {});

  // Step 2: Authenticate via browser WebAuthn API
  const credential = await startAuthentication({ optionsJSON: options });

  // Step 3: Verify with server, get JWT
  const result = await authFetch('/auth/login/complete', { challengeId, credential });

  if (result.verified && result.token) {
    storeAuth(result.token, result.userId);
    log.info('passkey login successful');
    return result;
  }

  throw new Error('Login verification failed');
}

// ── Status ──

export function getIdentityStatus() {
  return {
    supported: isPasskeySupported(),
    authenticated: isAuthenticated(),
    userId: localStorage.getItem(STORAGE_KEYS.userId),
  };
}
