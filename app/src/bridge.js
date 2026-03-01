// bridge.js — Gap bridge post-dictation UI

import { toggleDevice } from './form.js';
import { handleLabFiles } from './lab-import.js';
import { createLogger } from './logger.js';
const log = createLogger('bridge');

// computeResults is injected to avoid circular dependency
let _computeResults = null;
export function setComputeResults(fn) { _computeResults = fn; }

export function showGapBridge(extracted) {
  const bridge = document.getElementById('gap-bridge');
  const prompts = document.getElementById('bridge-prompts');
  const summary = document.getElementById('bridge-summary');

  const captured = [];
  if (extracted.age) captured.push('age');
  if (extracted.sex) captured.push('sex');
  if (extracted.height_feet || extracted.heightFt) captured.push('height');
  if (extracted.weight_lbs || extracted.weight) captured.push('weight');
  if (extracted.systolic) captured.push('blood pressure');
  if (extracted.waist_inches || extracted.waist) captured.push('waist');
  if (extracted.has_medications != null) captured.push('medications');
  if (extracted.has_family_history != null || extracted.familyHistory != null) captured.push('family history');
  const labCount = extracted.labs ? Object.keys(extracted.labs).length : 0;
  if (labCount > 0) captured.push(`${labCount} lab value${labCount !== 1 ? 's' : ''}`);

  summary.innerHTML = `Captured <strong>${captured.length} field${captured.length !== 1 ? 's' : ''}</strong> from your voice: ${captured.join(', ')}.`;

  let html = '';
  const hasLabs = labCount > 0 || extracted.has_labs === false;

  if (!hasLabs || labCount < 3) {
    const impact = hasLabs ? 'up to +15 pts' : 'up to +30 pts';
    html += `
      <div class="bridge-prompt" id="bridge-labs">
        <div class="bridge-prompt-header">
          <span class="bridge-prompt-title">Lab results</span>
          <span class="bridge-prompt-impact">${impact}</span>
        </div>
        <div class="bridge-prompt-hint">${labCount > 0 ? `You mentioned ${labCount} value${labCount !== 1 ? 's' : ''}. A full panel would fill the rest.` : 'Lipids, metabolic panel, ApoB — these are the biggest score drivers.'}</div>
        <div class="upload-zone" id="bridge-lab-drop" onclick="document.getElementById('bridge-lab-input').click()">
          <div class="icon">&darr;</div>
          <div class="uz-title">Drop a lab PDF here</div>
          <div class="uz-hint">Quest, LabCorp, hospital — any format</div>
        </div>
        <input type="file" id="bridge-lab-input" accept=".pdf,.txt,.csv" multiple style="display:none" onchange="handleBridgeLabImport(event)">
        <div class="parse-summary" id="bridge-lab-summary"></div>
      </div>`;
  }

  const hasWearable = extracted.resting_hr || extracted.daily_steps || extracted.sleep_hours;
  if (!hasWearable) {
    html += `
      <div class="bridge-prompt" id="bridge-wearable">
        <div class="bridge-prompt-header">
          <span class="bridge-prompt-title">Wearable data</span>
          <span class="bridge-prompt-impact">up to +10 pts</span>
        </div>
        <div class="bridge-prompt-hint">Steps, resting heart rate, sleep — we can pull these from your device.</div>
        <div class="device-grid" id="bridge-device-selector">
          <div class="device-card" data-device="apple_watch" onclick="toggleDevice(this)">
            <div class="device-icon">&#9201;</div>
            <div class="device-name">Apple Watch</div>
          </div>
          <div class="device-card" data-device="garmin" onclick="toggleDevice(this)">
            <div class="device-icon">&#9650;</div>
            <div class="device-name">Garmin</div>
          </div>
          <div class="device-card" data-device="oura" onclick="toggleDevice(this)">
            <div class="device-icon">&#9711;</div>
            <div class="device-name">Oura</div>
          </div>
          <div class="device-card" data-device="whoop" onclick="toggleDevice(this)">
            <div class="device-icon">&#9644;</div>
            <div class="device-name">WHOOP</div>
          </div>
          <div class="device-card" data-device="fitbit" onclick="toggleDevice(this)">
            <div class="device-icon">&#9632;</div>
            <div class="device-name">Fitbit</div>
          </div>
          <div class="device-card" data-device="none" onclick="toggleDevice(this)">
            <div class="device-icon" style="opacity:0.25;">&#10005;</div>
            <div class="device-name">None</div>
          </div>
        </div>
        <div class="device-notify">Select all that apply &middot; integrations coming soon</div>
      </div>`;
  }

  if (!html) {
    if (_computeResults) _computeResults();
    return;
  }

  prompts.innerHTML = html;

  // Wire up lab drop zone
  const bridgeDrop = document.getElementById('bridge-lab-drop');
  if (bridgeDrop) {
    bridgeDrop.addEventListener('dragover', (e) => { e.preventDefault(); bridgeDrop.classList.add('dragover'); });
    bridgeDrop.addEventListener('dragleave', () => bridgeDrop.classList.remove('dragover'));
    bridgeDrop.addEventListener('drop', (e) => {
      e.preventDefault();
      bridgeDrop.classList.remove('dragover');
      if (e.dataTransfer.files.length) {
        bridgeImportLabs(Array.from(e.dataTransfer.files));
      }
    });
  }

  document.getElementById('voice-hero').style.display = 'none';
  document.getElementById('intake-tabs').style.display = 'none';
  bridge.classList.add('active');
  window.scrollTo({ top: 0, behavior: 'smooth' });
  log.info('gap bridge shown', { captured: captured.length });
}

export function handleBridgeLabImport(event) {
  const files = Array.from(event.target.files);
  if (files.length) {
    bridgeImportLabs(files);
  }
}

function bridgeImportLabs(files) {
  const input = document.getElementById('lab-file-input');
  const dt = new DataTransfer();
  files.forEach(f => dt.items.add(f));
  input.files = dt.files;
  handleLabFiles(input.files);

  const summary = document.getElementById('bridge-lab-summary');
  if (summary) {
    summary.innerHTML = `<div class="bridge-imported">&#10003; ${files.length} file${files.length !== 1 ? 's' : ''} imported — values extracted</div>`;
  }
}

export async function bridgeScore() {
  if (_computeResults) await _computeResults();
}
