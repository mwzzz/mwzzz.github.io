export type BookmarkFolder = {
  id: string;
  name: string;
  description: string;
  createdAt: number;
};

export type BookmarkItem = {
  id: string;
  folderId: string;
  title: string;
  url: string;
  note: string;
  createdAt: number;
};

export type BookmarkStore = {
  folders: BookmarkFolder[];
  items: BookmarkItem[];
  activeFolderId: string | null;
};

export const STORAGE_KEY = 'mwzzz-bookmarks:v1';

function createId(): string {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  return `b-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

function emptyStore(): BookmarkStore {
  return { folders: [], items: [], activeFolderId: null };
}

export function loadStore(): BookmarkStore {
  if (typeof localStorage === 'undefined') return emptyStore();
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return emptyStore();
    const parsed = JSON.parse(raw) as Partial<BookmarkStore>;
    const folders = Array.isArray(parsed.folders) ? parsed.folders : [];
    const items = Array.isArray(parsed.items) ? parsed.items : [];
    let activeFolderId =
      typeof parsed.activeFolderId === 'string' ? parsed.activeFolderId : null;
    if (activeFolderId && !folders.some((f) => f.id === activeFolderId)) {
      activeFolderId = folders[0]?.id ?? null;
    }
    if (!activeFolderId && folders[0]) activeFolderId = folders[0].id;
    return { folders, items, activeFolderId };
  } catch {
    return emptyStore();
  }
}

export function saveStore(store: BookmarkStore): void {
  if (typeof localStorage === 'undefined') return;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(store));
}

/** Normalize URL: add https:// if scheme missing; return null if invalid */
export function normalizeUrl(input: string): string | null {
  const trimmed = input.trim();
  if (!trimmed) return null;
  let candidate = trimmed;
  if (!/^https?:\/\//i.test(candidate)) {
    candidate = `https://${candidate}`;
  }
  try {
    const url = new URL(candidate);
    if (url.protocol !== 'http:' && url.protocol !== 'https:') return null;
    if (!url.hostname.includes('.')) return null;
    return url.toString();
  } catch {
    return null;
  }
}

export function getActiveFolder(store: BookmarkStore): BookmarkFolder | null {
  if (!store.activeFolderId) return null;
  return store.folders.find((f) => f.id === store.activeFolderId) ?? null;
}

export function getItemsForFolder(store: BookmarkStore, folderId: string): BookmarkItem[] {
  return store.items
    .filter((item) => item.folderId === folderId)
    .sort((a, b) => b.createdAt - a.createdAt);
}

export function setActiveFolder(store: BookmarkStore, folderId: string | null): BookmarkStore {
  const next = { ...store, activeFolderId: folderId };
  saveStore(next);
  return next;
}

export function createFolder(
  store: BookmarkStore,
  name: string,
  description = '',
): BookmarkStore {
  const trimmed = name.trim();
  if (!trimmed) return store;

  const folder: BookmarkFolder = {
    id: createId(),
    name: trimmed,
    description: description.trim(),
    createdAt: Date.now(),
  };

  const next: BookmarkStore = {
    folders: [folder, ...store.folders],
    items: store.items,
    activeFolderId: folder.id,
  };
  saveStore(next);
  return next;
}

export function renameFolder(
  store: BookmarkStore,
  folderId: string,
  name: string,
  description?: string,
): BookmarkStore {
  const trimmed = name.trim();
  if (!trimmed) return store;

  const next: BookmarkStore = {
    ...store,
    folders: store.folders.map((folder) =>
      folder.id === folderId
        ? {
            ...folder,
            name: trimmed,
            description:
              typeof description === 'string' ? description.trim() : folder.description,
          }
        : folder,
    ),
  };
  saveStore(next);
  return next;
}

export function deleteFolder(store: BookmarkStore, folderId: string): BookmarkStore {
  const folders = store.folders.filter((f) => f.id !== folderId);
  const items = store.items.filter((item) => item.folderId !== folderId);
  let activeFolderId = store.activeFolderId;
  if (activeFolderId === folderId) {
    activeFolderId = folders[0]?.id ?? null;
  }
  const next = { folders, items, activeFolderId };
  saveStore(next);
  return next;
}

export function addItem(
  store: BookmarkStore,
  folderId: string,
  title: string,
  urlInput: string,
  note = '',
): { store: BookmarkStore; error?: string } {
  if (!store.folders.some((f) => f.id === folderId)) {
    return { store, error: '请先选择一个收藏夹' };
  }
  const trimmedTitle = title.trim();
  if (!trimmedTitle) return { store, error: '请填写标题' };

  const url = normalizeUrl(urlInput);
  if (!url) return { store, error: '链接无效，请检查后重试' };

  const item: BookmarkItem = {
    id: createId(),
    folderId,
    title: trimmedTitle,
    url,
    note: note.trim(),
    createdAt: Date.now(),
  };

  const next: BookmarkStore = {
    ...store,
    items: [item, ...store.items],
  };
  saveStore(next);
  return { store: next };
}

export function deleteItem(store: BookmarkStore, itemId: string): BookmarkStore {
  const next = {
    ...store,
    items: store.items.filter((item) => item.id !== itemId),
  };
  saveStore(next);
  return next;
}

export function countItems(store: BookmarkStore, folderId: string): number {
  return store.items.filter((item) => item.folderId === folderId).length;
}
