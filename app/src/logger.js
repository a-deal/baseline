// logger.js — Structured ring-buffer logger for Baseline
// Usage: const log = createLogger('intake'); log.info('message', { data });

const MAX_ENTRIES = 500;
const entries = [];

const LEVELS = { debug: 0, info: 1, warn: 2, error: 3 };

function push(entry) {
  entries.push(entry);
  if (entries.length > MAX_ENTRIES) entries.shift();
}

function formatConsole(entry) {
  const prefix = `[${entry.module}]`;
  const style = {
    debug: 'color: #6a6a7a',
    info: 'color: #9a9aaa',
    warn: 'color: #d4a24c',
    error: 'color: #c83c3c',
  }[entry.level] || '';

  if (entry.data !== undefined) {
    console.groupCollapsed(`%c${prefix} ${entry.msg}`, style);
    console.log(entry.data);
    console.log(`${entry.ts}`);
    console.groupEnd();
  } else {
    console[entry.level]?.(`%c${prefix} ${entry.msg}`, style) ||
      console.log(`%c${prefix} ${entry.msg}`, style);
  }
}

export function createLogger(module) {
  const log = (level, msg, data) => {
    const entry = {
      ts: new Date().toISOString(),
      level,
      module,
      msg,
      ...(data !== undefined && { data }),
    };
    push(entry);
    formatConsole(entry);
  };

  return {
    debug: (msg, data) => log('debug', msg, data),
    info: (msg, data) => log('info', msg, data),
    warn: (msg, data) => log('warn', msg, data),
    error: (msg, data) => log('error', msg, data),
  };
}

export const logger = {
  /** Return all log entries as a JSON string */
  dump() {
    return JSON.stringify(entries, null, 2);
  },

  /** Return last N entries, formatted for console reading */
  tail(n = 20) {
    return entries.slice(-n).map(e =>
      `${e.ts.slice(11, 23)} [${e.level}] [${e.module}] ${e.msg}${e.data ? ' ' + JSON.stringify(e.data) : ''}`
    ).join('\n');
  },

  /** Raw entries array */
  get entries() {
    return entries;
  },
};

// Expose globally for devtools access
if (typeof window !== 'undefined') {
  window.__baseline_logs = logger;
}
