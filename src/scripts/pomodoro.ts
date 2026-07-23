export type Phase = 'focus' | 'shortBreak' | 'longBreak';

export type PomodoroSettings = {
  focusMin: number;
  shortBreakMin: number;
  longBreakMin: number;
  longBreakEvery: number;
};

export type PomodoroState = {
  settings: PomodoroSettings;
  todayKey: string;
  completedToday: number;
  phase: Phase;
  /** Absolute end timestamp when running; null when paused/idle */
  endsAt: number | null;
  /** Remaining ms when paused or idle */
  remainingMs: number;
  running: boolean;
  focusStreak: number;
};

export const STORAGE_KEY = 'mwzzz-pomodoro:v1';
export const DEFAULT_TITLE = '番茄钟 · 敲码小站';

export const PHASE_LABEL: Record<Phase, string> = {
  focus: '专注',
  shortBreak: '短休',
  longBreak: '长休',
};

const DEFAULT_SETTINGS: PomodoroSettings = {
  focusMin: 25,
  shortBreakMin: 5,
  longBreakMin: 15,
  longBreakEvery: 4,
};

function pad(n: number) {
  return String(n).padStart(2, '0');
}

export function getTodayKey(date = new Date()): string {
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
}

export function minutesToMs(min: number): number {
  return Math.max(1, min) * 60 * 1000;
}

export function formatMs(ms: number): string {
  const total = Math.max(0, Math.ceil(ms / 1000));
  const m = Math.floor(total / 60);
  const s = total % 60;
  return `${pad(m)}:${pad(s)}`;
}

export function phaseDurationMs(settings: PomodoroSettings, phase: Phase): number {
  if (phase === 'focus') return minutesToMs(settings.focusMin);
  if (phase === 'shortBreak') return minutesToMs(settings.shortBreakMin);
  return minutesToMs(settings.longBreakMin);
}

function clampSettings(raw: Partial<PomodoroSettings> | undefined): PomodoroSettings {
  const n = (v: unknown, fallback: number, min: number, max: number) => {
    const num = typeof v === 'number' && Number.isFinite(v) ? v : fallback;
    return Math.min(max, Math.max(min, Math.round(num)));
  };
  return {
    focusMin: n(raw?.focusMin, DEFAULT_SETTINGS.focusMin, 1, 90),
    shortBreakMin: n(raw?.shortBreakMin, DEFAULT_SETTINGS.shortBreakMin, 1, 30),
    longBreakMin: n(raw?.longBreakMin, DEFAULT_SETTINGS.longBreakMin, 1, 60),
    longBreakEvery: n(raw?.longBreakEvery, DEFAULT_SETTINGS.longBreakEvery, 2, 8),
  };
}

function defaultState(): PomodoroState {
  const settings = { ...DEFAULT_SETTINGS };
  return {
    settings,
    todayKey: getTodayKey(),
    completedToday: 0,
    phase: 'focus',
    endsAt: null,
    remainingMs: phaseDurationMs(settings, 'focus'),
    running: false,
    focusStreak: 0,
  };
}

function readRaw(): Partial<PomodoroState> | null {
  if (typeof localStorage === 'undefined') return null;
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    return JSON.parse(raw) as Partial<PomodoroState>;
  } catch {
    return null;
  }
}

export function loadState(): PomodoroState {
  const base = defaultState();
  const raw = readRaw();
  if (!raw) return base;

  const settings = clampSettings(raw.settings);
  const today = getTodayKey();
  const sameDay = raw.todayKey === today;

  let state: PomodoroState = {
    settings,
    todayKey: today,
    completedToday: sameDay && typeof raw.completedToday === 'number' ? raw.completedToday : 0,
    phase: raw.phase === 'shortBreak' || raw.phase === 'longBreak' || raw.phase === 'focus' ? raw.phase : 'focus',
    endsAt: typeof raw.endsAt === 'number' ? raw.endsAt : null,
    remainingMs:
      typeof raw.remainingMs === 'number' ? raw.remainingMs : phaseDurationMs(settings, 'focus'),
    running: Boolean(raw.running),
    focusStreak: sameDay && typeof raw.focusStreak === 'number' ? raw.focusStreak : 0,
  };

  if (!sameDay) {
    state.running = false;
    state.endsAt = null;
    state.phase = 'focus';
    state.remainingMs = phaseDurationMs(settings, 'focus');
    state.focusStreak = 0;
  }

  return syncRemaining(state);
}

export function saveState(state: PomodoroState): void {
  if (typeof localStorage === 'undefined') return;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

/** Recompute remaining from endsAt when running */
export function syncRemaining(state: PomodoroState): PomodoroState {
  if (!state.running || state.endsAt == null) {
    return { ...state, running: false, endsAt: null };
  }
  const remainingMs = Math.max(0, state.endsAt - Date.now());
  return { ...state, remainingMs };
}

export function start(state: PomodoroState): PomodoroState {
  const synced = syncRemaining(state);
  if (synced.running) return synced;
  const remainingMs =
    synced.remainingMs > 0 ? synced.remainingMs : phaseDurationMs(synced.settings, synced.phase);
  return {
    ...synced,
    running: true,
    remainingMs,
    endsAt: Date.now() + remainingMs,
  };
}

export function pause(state: PomodoroState): PomodoroState {
  const synced = syncRemaining(state);
  return {
    ...synced,
    running: false,
    endsAt: null,
  };
}

export function reset(state: PomodoroState): PomodoroState {
  return {
    ...state,
    phase: 'focus',
    running: false,
    endsAt: null,
    remainingMs: phaseDurationMs(state.settings, 'focus'),
  };
}

export function updateSettings(
  state: PomodoroState,
  next: Partial<PomodoroSettings>,
): PomodoroState {
  const settings = clampSettings({ ...state.settings, ...next });
  // Don't interrupt an active run; new durations apply on reset / next phase setup
  if (state.running) {
    return { ...state, settings };
  }
  return {
    ...state,
    settings,
    remainingMs: phaseDurationMs(settings, state.phase),
    endsAt: null,
  };
}

function nextPhaseAfterFocus(state: PomodoroState): { phase: Phase; focusStreak: number; completedToday: number } {
  const streak = state.focusStreak + 1;
  const completedToday = state.completedToday + 1;
  const isLong = streak % state.settings.longBreakEvery === 0;
  return {
    phase: isLong ? 'longBreak' : 'shortBreak',
    focusStreak: streak,
    completedToday,
  };
}

/** Advance when remaining hits 0. Returns [newState, justCompletedFocus] */
export function completePhase(state: PomodoroState): { state: PomodoroState; completedFocus: boolean } {
  let completedFocus = false;
  let phase: Phase = 'focus';
  let focusStreak = state.focusStreak;
  let completedToday = state.completedToday;

  if (state.phase === 'focus') {
    completedFocus = true;
    const next = nextPhaseAfterFocus(state);
    phase = next.phase;
    focusStreak = next.focusStreak;
    completedToday = next.completedToday;
  } else {
    phase = 'focus';
  }

  const remainingMs = phaseDurationMs(state.settings, phase);
  const nextState: PomodoroState = {
    ...state,
    phase,
    focusStreak,
    completedToday,
    todayKey: getTodayKey(),
    running: false,
    endsAt: null,
    remainingMs,
  };

  return { state: nextState, completedFocus };
}

export function tick(state: PomodoroState): { state: PomodoroState; completedFocus: boolean; phaseEnded: boolean } {
  if (!state.running || state.endsAt == null) {
    return { state: syncRemaining(state), completedFocus: false, phaseEnded: false };
  }

  const remainingMs = state.endsAt - Date.now();
  if (remainingMs > 0) {
    return {
      state: { ...state, remainingMs },
      completedFocus: false,
      phaseEnded: false,
    };
  }

  const { state: next, completedFocus } = completePhase(state);
  return { state: next, completedFocus, phaseEnded: true };
}

export function playChime(): void {
  try {
    const Ctx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
    if (!Ctx) return;
    const ctx = new Ctx();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.value = 880;
    gain.gain.value = 0.08;
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start();
    gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.45);
    osc.stop(ctx.currentTime + 0.5);
    osc.onended = () => ctx.close();
  } catch {
    // ignore autoplay / unsupported
  }
}
