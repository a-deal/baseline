// Shared constants and utilities for Cut Tracker dashboard pages

window.CUT = {
  startDate: '2026-01-23',
  endDate: '2026-04-07',
  startWeight: 203.0,
  targetWeight: 188.0,
  totalDays: 74,
  peakTotal: 1290,
  peaks: { deadlift: 550, squat: 425, bench: 315 },
  macroTargets: { protein: 190, carbs: 180, fat: 60, calories: 2100 }
};

window.LIFT_COLORS = { deadlift: 'var(--blue)', squat: 'var(--amber)', bench: 'var(--accent)' };

window.parseCSV = function(text) {
  const lines = text.trim().split('\n');
  const headers = lines[0].split(',').map(h => h.trim());
  return lines.slice(1).filter(l => l.trim()).map(line => {
    const vals = line.split(',');
    const obj = {};
    headers.forEach((h, i) => obj[h] = vals[i]?.trim() ?? '');
    return obj;
  });
};

window.dayIndex = function(dateStr) {
  const start = new Date('2026-01-23T00:00:00');
  const d = new Date(dateStr + 'T00:00:00');
  return Math.round((d - start) / 86400000);
};

window.dayToX = function(d) { return 40 + (d / CUT.totalDays) * 640; };
window.weightToY = function(w) { return 240 - (w - CUT.targetWeight) * 13.75; };

window.todayStr = function() { return new Date().toISOString().slice(0, 10); };

window.fmtDate = function(dateStr) {
  const d = new Date(dateStr + 'T00:00:00');
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
};

// RPE-based 1RM estimation: reps@RPE -> estimated reps in reserve (RIR) -> effective reps
window.est1RM = function(weight, reps, rpe) {
  const rir = rpe ? 10 - rpe : 0;
  const effectiveReps = reps + rir;
  return effectiveReps <= 0 ? weight : Math.round(weight * (1 + effectiveReps / 30));
};

window.safeFetch = async function(url, json) {
  try {
    const r = await fetch(url);
    if (!r.ok) return null;
    return json ? r.json() : r.text();
  } catch { return null; }
};
