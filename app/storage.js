/**
 * Baseline — localStorage Profile Persistence
 */

const STORAGE_KEY = 'baseline_profile';

function saveProfile(profile) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(profile));
  } catch (e) {
    console.warn('Failed to save profile:', e);
  }
}

function loadProfile() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch (e) {
    console.warn('Failed to load profile:', e);
    return null;
  }
}

function clearProfile() {
  localStorage.removeItem(STORAGE_KEY);
}

export { saveProfile, loadProfile, clearProfile };
