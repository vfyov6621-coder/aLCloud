// Zustand store for aLCloud state management
import { create } from 'zustand';
import { type FileItem, type StorageQuota, type ProviderType, PROVIDERS_INFO } from '@/lib/providers/types';

export type ViewMode = 'grid' | 'list';
export type SortField = 'name' | 'size' | 'date' | 'type';
export type SortDirection = 'asc' | 'desc';

export interface ConnectedProvider {
  id: string;
  providerType: string;
  displayName: string;
  isConnected: boolean;
  accountEmail?: string | null;
  accountName?: string | null;
  avatarUrl?: string | null;
  quota?: StorageQuota | null;
}

interface CloudState {
  // Data
  providers: ConnectedProvider[];
  files: FileItem[];
  currentPath: string[];
  viewMode: ViewMode;
  sortField: SortField;
  sortDirection: SortDirection;
  selectedProvider: string | null;
  searchQuery: string;
  selectedFiles: Set<string>;

  // UI State
  loading: boolean;
  uploading: boolean;
  uploadProgress: number;
  error: string | null;
  sidebarOpen: boolean;
  showConnectDialog: boolean;
  showFileInfo: FileItem | null;
  contextMenuFile: FileItem | null;

  // Actions
  setProviders: (providers: ConnectedProvider[]) => void;
  setFiles: (files: FileItem[]) => void;
  setCurrentPath: (path: string[]) => void;
  navigateTo: (path: string[]) => void;
  setViewMode: (mode: ViewMode) => void;
  setSortField: (field: SortField) => void;
  setSortDirection: (direction: SortDirection) => void;
  setSelectedProvider: (provider: string | null) => void;
  setSearchQuery: (query: string) => void;
  setSelectedFiles: (ids: Set<string>) => void;
  toggleFileSelection: (id: string) => void;
  clearSelection: () => void;
  selectAll: () => void;

  setLoading: (loading: boolean) => void;
  setUploading: (uploading: boolean) => void;
  setUploadProgress: (progress: number) => void;
  setError: (error: string | null) => void;
  setSidebarOpen: (open: boolean) => void;
  toggleSidebar: () => void;
  setShowConnectDialog: (show: boolean) => void;
  setShowFileInfo: (file: FileItem | null) => void;
  setContextMenuFile: (file: FileItem | null) => void;

  connectProvider: (providerType: string) => void;
  disconnectProvider: (id: string) => void;
  fetchFiles: () => Promise<void>;
  searchFiles: (query: string) => Promise<void>;
  deleteFile: (id: string) => void;

  getSortedFiles: () => FileItem[];
  getFilteredFiles: () => FileItem[];
}

export const useCloudStore = create<CloudState>((set, get) => ({
  // Initial State
  providers: [],
  files: [],
  currentPath: [],
  viewMode: 'grid',
  sortField: 'name',
  sortDirection: 'asc',
  selectedProvider: null,
  searchQuery: '',
  selectedFiles: new Set(),

  loading: false,
  uploading: false,
  uploadProgress: 0,
  error: null,
  sidebarOpen: true,
  showConnectDialog: false,
  showFileInfo: null,
  contextMenuFile: null,

  // Setters
  setProviders: (providers) => set({ providers }),
  setFiles: (files) => set({ files }),
  setCurrentPath: (path) => set({ currentPath: path }),

  navigateTo: (path) => {
    set({ currentPath: path, selectedFiles: new Set() });
    // Trigger file fetch for new path
    get().fetchFiles();
  },

  setViewMode: (mode) => set({ viewMode: mode }),
  setSortField: (field) => set({ sortField: field }),
  setSortDirection: (direction) => set({ sortDirection: direction }),
  setSelectedProvider: (provider) => {
    set({ selectedProvider: provider, currentPath: [], selectedFiles: new Set() });
    get().fetchFiles();
  },
  setSearchQuery: (query) => set({ searchQuery: query }),
  setSelectedFiles: (ids) => set({ selectedFiles: ids }),

  toggleFileSelection: (id) => {
    const selected = new Set(get().selectedFiles);
    if (selected.has(id)) {
      selected.delete(id);
    } else {
      selected.add(id);
    }
    set({ selectedFiles: selected });
  },

  clearSelection: () => set({ selectedFiles: new Set() }),

  selectAll: () => {
    const files = get().files;
    set({ selectedFiles: new Set(files.map(f => f.id)) });
  },

  setLoading: (loading) => set({ loading }),
  setUploading: (uploading) => set({ uploading }),
  setUploadProgress: (progress) => set({ uploadProgress: progress }),
  setError: (error) => set({ error }),
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setShowConnectDialog: (show) => set({ showConnectDialog: show }),
  setShowFileInfo: (file) => set({ showFileInfo: file }),
  setContextMenuFile: (file) => set({ contextMenuFile: file }),

  connectProvider: (providerType) => {
    const info = PROVIDERS_INFO[providerType as ProviderType];
    if (!info) return;

    const newProvider: ConnectedProvider = {
      id: `conn-${providerType}-${Date.now()}`,
      providerType,
      displayName: info.name,
      isConnected: true,
      accountEmail: `user@${info.name.toLowerCase().replace(/\s/g, '').replace('.', '')}.com`,
      accountName: 'Demo User',
    };

    const existing = get().providers;
    const alreadyConnected = existing.find(p => p.providerType === providerType && p.isConnected);
    if (alreadyConnected) return;

    set({
      providers: [...existing, newProvider],
      selectedProvider: providerType,
      showConnectDialog: false,
    });

    get().fetchFiles();
  },

  disconnectProvider: (id) => {
    set((state) => {
      const updated = state.providers.map(p =>
        p.id === id ? { ...p, isConnected: false } : p
      );
      const selectedProvider = state.selectedProvider;
      const disconnected = state.providers.find(p => p.id === id);
      const newSelected = (disconnected && disconnected.providerType === selectedProvider)
        ? updated.find(p => p.isConnected)?.providerType || null
        : selectedProvider;

      return {
        providers: updated,
        selectedProvider: newSelected,
        files: [],
        currentPath: [],
      };
    });
  },

  fetchFiles: async () => {
    const { selectedProvider, currentPath } = get();
    if (!selectedProvider) {
      set({ files: [] });
      return;
    }

    set({ loading: true, error: null });

    try {
      const path = currentPath.length > 0 ? '/' + currentPath.join('/') : '/';
      const res = await fetch(
        `/api/providers/${selectedProvider}/files?path=${encodeURIComponent(path)}`
      );
      if (!res.ok) throw new Error('Failed to fetch files');
      const data = await res.json();
      set({ files: data.files || [], loading: false });
    } catch (err) {
      set({
        error: err instanceof Error ? err.message : 'Failed to fetch files',
        loading: false,
      });
    }
  },

  searchFiles: async (query) => {
    if (!query.trim()) {
      get().fetchFiles();
      return;
    }

    set({ loading: true, searchQuery: query });

    try {
      const { selectedProvider } = get();
      let url = '/api/files';
      const params = new URLSearchParams({ query });
      if (selectedProvider) params.set('provider', selectedProvider);
      url += `?${params.toString()}`;

      const res = await fetch(url);
      if (!res.ok) throw new Error('Search failed');
      const data = await res.json();
      set({ files: data.files || [], loading: false });
    } catch (err) {
      set({
        error: err instanceof Error ? err.message : 'Search failed',
        loading: false,
      });
    }
  },

  deleteFile: (id) => {
    set((state) => ({
      files: state.files.filter(f => f.id !== id),
      selectedFiles: (() => {
        const s = new Set(state.selectedFiles);
        s.delete(id);
        return s;
      })(),
      showFileInfo: state.showFileInfo?.id === id ? null : state.showFileInfo,
    }));
  },

  getSortedFiles: () => {
    const { files, sortField, sortDirection } = get();
    const sorted = [...files].sort((a, b) => {
      // Folders always come first
      if (a.type === 'folder' && b.type !== 'folder') return -1;
      if (a.type !== 'folder' && b.type === 'folder') return 1;

      let comparison = 0;
      switch (sortField) {
        case 'name':
          comparison = a.name.localeCompare(b.name);
          break;
        case 'size':
          comparison = a.size - b.size;
          break;
        case 'date':
          comparison = new Date(a.lastModified).getTime() - new Date(b.lastModified).getTime();
          break;
        case 'type':
          comparison = (a.mimeType || '').localeCompare(b.mimeType || '');
          break;
      }
      return sortDirection === 'asc' ? comparison : -comparison;
    });
    return sorted;
  },

  getFilteredFiles: () => {
    const { searchQuery } = get();
    const sorted = get().getSortedFiles();

    if (!searchQuery) return sorted;
    const query = searchQuery.toLowerCase();
    return sorted.filter(
      f => f.name.toLowerCase().includes(query) || f.mimeType?.toLowerCase().includes(query)
    );
  },
}));
