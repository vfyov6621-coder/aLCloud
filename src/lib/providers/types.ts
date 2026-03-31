// Provider types and interfaces for aLCloud

export enum ProviderType {
  GOOGLE_DRIVE = 'google-drive',
  TELEGRAM = 'telegram',
  YANDEX_DISK = 'yandex-disk',
  MAILRU_CLOUD = 'mailru-cloud',
  GITHUB = 'github',
}

export interface ProviderInfo {
  type: ProviderType;
  name: string;
  description: string;
  icon: string;
  color: string;
  authUrl?: string;
}

export interface FileItem {
  id: string;
  name: string;
  path: string;
  parentId?: string | null;
  size: number;
  mimeType?: string | null;
  type: 'file' | 'folder';
  providerId: string;
  providerFileId?: string | null;
  thumbnail?: string | null;
  lastModified: Date;
  isStarred: boolean;
  isShared: boolean;
}

export interface StorageQuota {
  used: number;
  total: number;
  usedLabel: string;
  totalLabel: string;
}

export interface AuthResult {
  success: boolean;
  accessToken?: string;
  refreshToken?: string;
  expiresAt?: Date;
  accountEmail?: string;
  accountName?: string;
  avatarUrl?: string;
  error?: string;
}

export interface ListResult {
  files: FileItem[];
  hasNextPage: boolean;
  nextCursor?: string;
}

export interface SearchOptions {
  query: string;
  pageSize?: number;
  pageToken?: string;
}

export interface UploadOptions {
  file: File;
  path: string;
  onProgress?: (progress: number) => void;
}

export interface DownloadResult {
  blob: Blob;
  fileName: string;
  mimeType: string;
}

export interface IProvider {
  readonly type: ProviderType;
  readonly info: ProviderInfo;

  authenticate(authCode: string): Promise<AuthResult>;
  getAuthUrl(): string;
  list(path?: string, pageToken?: string): Promise<ListResult>;
  search(options: SearchOptions): Promise<ListResult>;
  upload(options: UploadOptions): Promise<FileItem>;
  download(fileId: string): Promise<DownloadResult>;
  delete(fileId: string): Promise<void>;
  getQuota(): Promise<StorageQuota>;
  refreshAccessToken?(refreshToken: string): Promise<AuthResult>;
}

export const PROVIDERS_INFO: Record<ProviderType, ProviderInfo> = {
  [ProviderType.GOOGLE_DRIVE]: {
    type: ProviderType.GOOGLE_DRIVE,
    name: 'Google Drive',
    description: 'Access your Google Drive files and folders',
    icon: 'google-drive',
    color: '#4285F4',
  },
  [ProviderType.TELEGRAM]: {
    type: ProviderType.TELEGRAM,
    name: 'Telegram',
    description: 'Access files shared in your Telegram chats',
    icon: 'telegram',
    color: '#26A5E4',
  },
  [ProviderType.YANDEX_DISK]: {
    type: ProviderType.YANDEX_DISK,
    name: 'Yandex.Disk',
    description: 'Access your Yandex.Disk cloud storage',
    icon: 'yandex-disk',
    color: '#FC3F1D',
  },
  [ProviderType.MAILRU_CLOUD]: {
    type: ProviderType.MAILRU_CLOUD,
    name: 'Mail.ru Cloud',
    description: 'Access your Mail.ru Cloud storage',
    icon: 'mail-ru',
    color: '#005FF9',
  },
  [ProviderType.GITHUB]: {
    type: ProviderType.GITHUB,
    name: 'GitHub',
    description: 'Access your GitHub repositories and releases',
    icon: 'github',
    color: '#6E40C9',
  },
};

export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`;
}

export function getFileExtension(filename: string): string {
  const parts = filename.split('.');
  return parts.length > 1 ? parts[parts.length - 1].toLowerCase() : '';
}

export function getFileIcon(mimeType?: string | null, filename?: string): string {
  if (!mimeType && !filename) return 'file';
  if (mimeType?.startsWith('image/')) return 'image';
  if (mimeType?.startsWith('video/')) return 'video';
  if (mimeType?.startsWith('audio/')) return 'music';
  if (mimeType === 'application/pdf') return 'file-text';
  if (mimeType?.includes('zip') || mimeType?.includes('rar') || mimeType?.includes('tar')) return 'archive';

  const ext = filename ? getFileExtension(filename) : '';
  if (['doc', 'docx', 'odt'].includes(ext)) return 'file-text';
  if (['xls', 'xlsx', 'ods', 'csv'].includes(ext)) return 'sheet';
  if (['ppt', 'pptx', 'odp'].includes(ext)) return 'presentation';
  if (['js', 'ts', 'py', 'java', 'cpp', 'c', 'html', 'css', 'json', 'xml', 'md'].includes(ext)) return 'code';
  if (['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp', 'bmp'].includes(ext)) return 'image';

  return 'file';
}

export function isFolder(item: FileItem): boolean {
  return item.type === 'folder';
}

// Demo/mock data generators for each provider
export function generateDemoFiles(providerType: ProviderType): FileItem[] {
  const now = new Date();
  const day = 24 * 60 * 60 * 1000;

  const baseFiles: FileItem[] = [
    {
      id: `demo-${providerType}-1`,
      name: 'Documents',
      path: '/Documents',
      size: 0,
      type: 'folder',
      providerId: providerType,
      lastModified: new Date(now - 2 * day),
      isStarred: true,
      isShared: false,
    },
    {
      id: `demo-${providerType}-2`,
      name: 'Photos',
      path: '/Photos',
      size: 0,
      type: 'folder',
      providerId: providerType,
      lastModified: new Date(now - 1 * day),
      isStarred: false,
      isShared: true,
    },
    {
      id: `demo-${providerType}-3`,
      name: 'Projects',
      path: '/Projects',
      size: 0,
      type: 'folder',
      providerId: providerType,
      lastModified: new Date(now - 5 * day),
      isStarred: true,
      isShared: false,
    },
    {
      id: `demo-${providerType}-4`,
      name: 'Vacation Planning.docx',
      path: '/Documents/Vacation Planning.docx',
      parentId: `demo-${providerType}-1`,
      size: 245760,
      mimeType: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      type: 'file',
      providerId: providerType,
      lastModified: new Date(now - 2 * day),
      isStarred: false,
      isShared: false,
    },
    {
      id: `demo-${providerType}-5`,
      name: 'Budget 2024.xlsx',
      path: '/Documents/Budget 2024.xlsx',
      parentId: `demo-${providerType}-1`,
      size: 189440,
      mimeType: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      type: 'file',
      providerId: providerType,
      lastModified: new Date(now - 3 * day),
      isStarred: true,
      isShared: true,
    },
    {
      id: `demo-${providerType}-6`,
      name: 'Beach Sunset.jpg',
      path: '/Photos/Beach Sunset.jpg',
      parentId: `demo-${providerType}-2`,
      size: 3145728,
      mimeType: 'image/jpeg',
      type: 'file',
      providerId: providerType,
      lastModified: new Date(now - 1 * day),
      isStarred: true,
      isShared: false,
    },
    {
      id: `demo-${providerType}-7`,
      name: 'Mountain View.png',
      path: '/Photos/Mountain View.png',
      parentId: `demo-${providerType}-2`,
      size: 5242880,
      mimeType: 'image/png',
      type: 'file',
      providerId: providerType,
      lastModified: new Date(now - 4 * day),
      isStarred: false,
      isShared: false,
    },
    {
      id: `demo-${providerType}-8`,
      name: 'Presentation.pdf',
      path: '/Projects/Presentation.pdf',
      parentId: `demo-${providerType}-3`,
      size: 1048576,
      mimeType: 'application/pdf',
      type: 'file',
      providerId: providerType,
      lastModified: new Date(now - 5 * day),
      isStarred: false,
      isShared: true,
    },
    {
      id: `demo-${providerType}-9`,
      name: 'README.md',
      path: '/Projects/README.md',
      parentId: `demo-${providerType}-3`,
      size: 4096,
      mimeType: 'text/markdown',
      type: 'file',
      providerId: providerType,
      lastModified: new Date(now - 6 * day),
      isStarred: false,
      isShared: false,
    },
    {
      id: `demo-${providerType}-10`,
      name: 'Source Code.zip',
      path: '/Projects/Source Code.zip',
      parentId: `demo-${providerType}-3`,
      size: 15728640,
      mimeType: 'application/zip',
      type: 'file',
      providerId: providerType,
      lastModified: new Date(now - 7 * day),
      isStarred: false,
      isShared: false,
    },
    {
      id: `demo-${providerType}-11`,
      name: 'Meeting Notes.txt',
      path: '/Meeting Notes.txt',
      size: 2048,
      mimeType: 'text/plain',
      type: 'file',
      providerId: providerType,
      lastModified: new Date(now - 0.5 * day),
      isStarred: false,
      isShared: false,
    },
    {
      id: `demo-${providerType}-12`,
      name: 'Music',
      path: '/Music',
      size: 0,
      type: 'folder',
      providerId: providerType,
      lastModified: new Date(now - 10 * day),
      isStarred: false,
      isShared: false,
    },
  ];

  return baseFiles;
}

export function generateDemoQuota(providerType: ProviderType): StorageQuota {
  const quotas: Record<ProviderType, StorageQuota> = {
    [ProviderType.GOOGLE_DRIVE]: {
      used: 7340032000,
      total: 16106127360,
      usedLabel: '6.8 GB',
      totalLabel: '15 GB',
    },
    [ProviderType.TELEGRAM]: {
      used: 2097152000,
      total: 4294967296,
      usedLabel: '2.0 GB',
      totalLabel: '4 GB',
    },
    [ProviderType.YANDEX_DISK]: {
      used: 3221225472,
      total: 5368709120,
      usedLabel: '3.0 GB',
      totalLabel: '5 GB',
    },
    [ProviderType.MAILRU_CLOUD]: {
      used: 858993459,
      total: 8589934592,
      usedLabel: '825 MB',
      totalLabel: '8 GB',
    },
    [ProviderType.GITHUB]: {
      used: 536870912,
      total: 1073741824,
      usedLabel: '512 MB',
      totalLabel: '1 GB',
    },
  };

  return quotas[providerType];
}
