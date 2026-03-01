// main.js — Entry point: imports, init sequence, window.* bindings

import { loadNhanes } from '../nhanes.js';
import { scoreTimeSeriesProfile } from '../score.js';
import { initStorage, loadFullProfile, saveDemographics, addImportWithObservations, saveManualObservations, clearAll } from '../storage.js';
import { exportAll, importAll } from '../db.js';
import { createLogger } from './logger.js';

import { initProgressBar, initToggleButtons, toggleDevice, nextStep, prevStep, showStep, buildProfile, populateForm, switchIntakeTab, addParsedLabValues, clearPendingImports, getPendingImports, resetState } from './form.js';
import { initLabDrop, handleLabFileInput, parseLabText, togglePasteLabs, toggleManualLabs } from './lab-import.js';
import { renderResults } from './render.js';
import { toggleFullVoice, toggleVoice, submitVoiceIntake, hasSpeechSupport, hideSpeechUI, resetVoiceState, checklistLocked, setShowGapBridge, applyExtraction, expandTranscript } from './intake.js';
import { initMedSearch, removeMedTag } from './meds.js';
import { showGapBridge, handleBridgeLabImport, bridgeScore, setComputeResults } from './bridge.js';

const log = createLogger('main');

// ── Wire up circular dependencies ──
setShowGapBridge(showGapBridge);
setComputeResults(computeResults);

// ── Init ──
log.info('baseline app starting');
await loadNhanes();
const persisted = await initStorage();
initProgressBar();
initToggleButtons();
initLabDrop();
initMedSearch();
await checkReturnVisit();
if (!persisted) {
  log.warn('storage not persistent — show export reminder after scoring');
}

// Hide voice tab if Speech API isn't available
if (!hasSpeechSupport()) {
  hideSpeechUI();
  switchIntakeTab('form');
}

log.info('baseline app ready');

// ── Compute & render results ──
async function computeResults() {
  const formProfile = buildProfile();

  await saveDemographics(formProfile.demographics);

  const pending = getPendingImports();
  for (const imp of pending) {
    await addImportWithObservations(imp.meta, imp.observations);
  }
  clearPendingImports();

  const manualFields = {};
  const manualMetrics = [
    ['systolic', formProfile.systolic], ['diastolic', formProfile.diastolic],
    ['waist_circumference', formProfile.waist_circumference],
    ['weight_lbs', formProfile.weight_lbs],
    ['resting_hr', formProfile.resting_hr], ['vo2_max', formProfile.vo2_max],
    ['hrv_rmssd_avg', formProfile.hrv_rmssd_avg],
    ['daily_steps_avg', formProfile.daily_steps_avg],
    ['sleep_duration_avg', formProfile.sleep_duration_avg],
    ['sleep_regularity_stddev', formProfile.sleep_regularity_stddev],
    ['zone2_min_per_week', formProfile.zone2_min_per_week],
    ['ldl_c', formProfile.ldl_c], ['hdl_c', formProfile.hdl_c],
    ['triglycerides', formProfile.triglycerides], ['apob', formProfile.apob],
    ['fasting_glucose', formProfile.fasting_glucose], ['fasting_insulin', formProfile.fasting_insulin],
    ['hba1c', formProfile.hba1c], ['lpa', formProfile.lpa], ['hscrp', formProfile.hscrp],
    ['alt', formProfile.alt], ['ggt', formProfile.ggt], ['tsh', formProfile.tsh],
    ['vitamin_d', formProfile.vitamin_d], ['ferritin', formProfile.ferritin],
    ['hemoglobin', formProfile.hemoglobin], ['wbc', formProfile.wbc], ['platelets', formProfile.platelets],
  ];
  for (const [key, val] of manualMetrics) {
    if (val != null) manualFields[key] = val;
  }
  if (formProfile.has_family_history != null) manualFields.has_family_history = formProfile.has_family_history;
  if (formProfile.has_medication_list != null) manualFields.has_medication_list = formProfile.has_medication_list;
  if (formProfile.phq9_score != null) manualFields.phq9_score = formProfile.phq9_score;

  if (Object.keys(manualFields).length > 0) {
    await saveManualObservations(manualFields);
  }

  const tsProfile = await loadFullProfile();
  const output = scoreTimeSeriesProfile(tsProfile);
  renderResults(output, formProfile);
  log.info('results computed', { score: output.coverageScore });
}

// ── Return visit ──
async function checkReturnVisit() {
  const profile = await loadFullProfile();
  const hasData = profile && Object.keys(profile.observations).length > 0;
  if (hasData) {
    const metricCount = Object.keys(profile.observations).length;
    const importCount = profile.imports?.length || 0;
    const banner = document.getElementById('return-banner');
    banner.querySelector('span').innerHTML =
      `Welcome back. <strong>${metricCount} metrics</strong> from ${importCount} import${importCount !== 1 ? 's' : ''} saved. Update or start fresh?`;
    banner.classList.add('active');
  }
}

// ── Window bindings for HTML onclick handlers ──
window.toggleFullVoice = toggleFullVoice;
window.toggleVoice = toggleVoice;
window.toggleDevice = toggleDevice;
window.nextStep = nextStep;
window.prevStep = prevStep;
window.switchIntakeTab = switchIntakeTab;
window.expandForm = () => switchIntakeTab('form');
window.showFormMode = () => switchIntakeTab('form');
window.submitVoiceIntake = submitVoiceIntake;
window.handleBridgeLabImport = handleBridgeLabImport;
window.bridgeScore = bridgeScore;
window.computeResults = computeResults;
window.parseLabText = parseLabText;
window.togglePasteLabs = togglePasteLabs;
window.toggleManualLabs = toggleManualLabs;
window.handleLabFileInput = handleLabFileInput;
window.expandTranscript = expandTranscript;
window.removeMedTag = removeMedTag;

window.loadSavedProfile = async function() {
  const tsProfile = await loadFullProfile();
  if (!tsProfile || Object.keys(tsProfile.observations).length === 0) return;
  document.getElementById('return-banner').classList.remove('active');
  const flat = { demographics: tsProfile.demographics };
  for (const [metric, obs] of Object.entries(tsProfile.observations)) {
    if (obs.length > 0) flat[metric] = obs[0].value;
  }
  populateForm(flat);
};

window.clearSaved = async function() {
  await clearAll();
  document.getElementById('return-banner').classList.remove('active');
};

window.startOver = function() {
  document.getElementById('results').classList.remove('active');
  document.getElementById('questionnaire').style.display = 'block';
  document.getElementById('gap-bridge').classList.remove('active');
  document.getElementById('voice-hero').style.display = '';
  document.getElementById('intake-tabs').style.display = '';
  switchIntakeTab('voice');
  document.getElementById('voice-idle').style.display = '';
  document.getElementById('voice-active').classList.remove('show');
  document.getElementById('voice-full-transcript').value = '';
  document.getElementById('voice-submit-btn').disabled = true;
  document.querySelectorAll('.voice-checklist-item').forEach(i => { i.classList.remove('checked', 'pending', 'declined'); });
  resetVoiceState();
  const guide = document.getElementById('voice-guide');
  if (guide) { const n = guide.querySelector('#guide-nudges'); if (n) n.innerHTML = ''; }
};

window.clearAndRestart = async function() {
  await clearAll();
  resetState();
  document.getElementById('results').classList.remove('active');
  document.getElementById('questionnaire').style.display = 'block';
  document.querySelectorAll('.field-input').forEach(i => i.value = '');
  document.querySelectorAll('.opt-btn, .toggle-btn').forEach(b => b.classList.remove('selected'));
  document.getElementById('lab-paste').value = '';
  document.getElementById('parse-results').classList.remove('active');
  document.getElementById('lab-file-list').innerHTML = '';
  document.querySelectorAll('.manual-fields').forEach(f => f.classList.remove('open'));
  document.getElementById('gap-bridge').classList.remove('active');
  document.getElementById('voice-hero').style.display = '';
  document.getElementById('intake-tabs').style.display = '';
  document.getElementById('voice-idle').style.display = '';
  document.getElementById('voice-active').classList.remove('show');
  document.getElementById('voice-full-transcript').value = '';
  document.getElementById('voice-submit-btn').disabled = true;
  document.querySelectorAll('.voice-checklist-item').forEach(i => { i.classList.remove('checked', 'pending', 'declined'); });
  resetVoiceState();
  const guideEl = document.getElementById('voice-guide');
  if (guideEl) { const n = guideEl.querySelector('#guide-nudges'); if (n) n.innerHTML = ''; }
  switchIntakeTab('voice');
};

window.exportProfile = async function() {
  const data = await exportAll();
  const json = JSON.stringify(data, null, 2);
  const blob = new Blob([json], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `baseline-profile-${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(url);
};

window.importProfile = async function() {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = '.json';
  input.onchange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    try {
      const text = await file.text();
      const data = JSON.parse(text);
      await importAll(data);
      window.location.reload();
    } catch (err) {
      alert('Failed to import profile: ' + err.message);
    }
  };
  input.click();
};
