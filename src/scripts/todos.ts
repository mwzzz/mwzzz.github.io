export type TodoItem = {
  id: string;
  text: string;
  done: boolean;
  createdAt: number;
};

export type TodoStore = Record<string, TodoItem[]>;

export const STORAGE_KEY = 'mwzzz-todos:v1';
const MAX_DAYS = 30;

function pad(n: number) {
  return String(n).padStart(2, '0');
}

/** Local timezone date key YYYY-MM-DD */
export function getDateKey(date = new Date()): string {
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
}

export function getTodayKey(): string {
  return getDateKey(new Date());
}

export function getYesterdayKey(): string {
  const d = new Date();
  d.setDate(d.getDate() - 1);
  return getDateKey(d);
}

export function formatDateLabel(key: string): string {
  const [y, m, day] = key.split('-').map(Number);
  const date = new Date(y, m - 1, day);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'short',
  });
}

export function createId(): string {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  return `t-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

function readStore(): TodoStore {
  if (typeof localStorage === 'undefined') return {};
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return {};
    const parsed = JSON.parse(raw) as TodoStore;
    return parsed && typeof parsed === 'object' ? parsed : {};
  } catch {
    return {};
  }
}

function writeStore(store: TodoStore): void {
  if (typeof localStorage === 'undefined') return;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(pruneStore(store)));
}

function pruneStore(store: TodoStore): TodoStore {
  const keys = Object.keys(store).sort();
  if (keys.length <= MAX_DAYS) return store;
  const keep = new Set(keys.slice(-MAX_DAYS));
  const next: TodoStore = {};
  for (const key of keys) {
    if (keep.has(key)) next[key] = store[key];
  }
  return next;
}

export function loadDay(dateKey: string): TodoItem[] {
  const store = readStore();
  return Array.isArray(store[dateKey]) ? store[dateKey] : [];
}

export function saveDay(dateKey: string, items: TodoItem[]): void {
  const store = readStore();
  store[dateKey] = items;
  writeStore(store);
}

/**
 * Ensure today's bucket exists. If today has no entry yet and yesterday
 * has unfinished items, carry them over with new ids.
 */
export function ensureToday(): TodoItem[] {
  const today = getTodayKey();
  const store = readStore();

  if (Object.prototype.hasOwnProperty.call(store, today)) {
    return Array.isArray(store[today]) ? store[today] : [];
  }

  const yesterday = getYesterdayKey();
  const prev = Array.isArray(store[yesterday]) ? store[yesterday] : [];
  const carried = prev
    .filter((item) => item && !item.done && item.text?.trim())
    .map((item) => ({
      id: createId(),
      text: item.text.trim(),
      done: false,
      createdAt: Date.now(),
    }));

  store[today] = carried;
  writeStore(store);
  return carried;
}

export function addTodo(text: string): TodoItem[] {
  const trimmed = text.trim();
  if (!trimmed) return ensureToday();

  const today = getTodayKey();
  const items = ensureToday();
  const next = [
    {
      id: createId(),
      text: trimmed,
      done: false,
      createdAt: Date.now(),
    },
    ...items,
  ];
  saveDay(today, next);
  return next;
}

export function toggleTodo(id: string): TodoItem[] {
  const today = getTodayKey();
  const items = ensureToday().map((item) =>
    item.id === id ? { ...item, done: !item.done } : item,
  );
  saveDay(today, items);
  return items;
}

export function removeTodo(id: string): TodoItem[] {
  const today = getTodayKey();
  const items = ensureToday().filter((item) => item.id !== id);
  saveDay(today, items);
  return items;
}

export function sortTodos(items: TodoItem[]): TodoItem[] {
  return [...items].sort((a, b) => {
    if (a.done !== b.done) return a.done ? 1 : -1;
    return b.createdAt - a.createdAt;
  });
}

export function getProgress(items: TodoItem[]): { done: number; total: number } {
  const total = items.length;
  const done = items.filter((item) => item.done).length;
  return { done, total };
}
