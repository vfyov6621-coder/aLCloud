// Abstract base provider class with common functionality
import {
  type IProvider,
  type FileItem,
  type StorageQuota,
  type AuthResult,
  type ListResult,
  type SearchOptions,
  type UploadOptions,
  type DownloadResult,
  type ProviderInfo,
  type ProviderType,
  generateDemoFiles,
  generateDemoQuota,
} from './types';

export abstract class BaseProvider implements IProvider {
  abstract readonly type: ProviderType;
  abstract readonly info: ProviderInfo;

  // Simulated authentication state for demo
  protected _isAuthenticated = false;
  protected _accessToken: string | null = null;

  get isAuthenticated(): boolean {
    return this._isAuthenticated;
  }

  abstract getAuthUrl(): string;

  async authenticate(_authCode: string): Promise<AuthResult> {
    // Default demo implementation - simulates successful auth
    this._isAuthenticated = true;
    this._accessToken = `demo-token-${this.type}-${Date.now()}`;
    
    return {
      success: true,
      accessToken: this._accessToken,
      refreshToken: `demo-refresh-${this.type}`,
      expiresAt: new Date(Date.now() + 3600 * 1000),
      accountEmail: `user@${this.info.name.toLowerCase().replace(/\s/g, '')}.com`,
      accountName: 'Demo User',
    };
  }

  async list(_path?: string, _pageToken?: string): Promise<ListResult> {
    // Default demo implementation returns mock files
    const files = generateDemoFiles(this.type);
    
    if (_path && _path !== '/') {
      const folderName = _path.split('/').filter(Boolean).pop();
      return {
        files: files.filter(f => f.parentId && f.path.includes(folderName || '')),
        hasNextPage: false,
      };
    }

    return {
      files: files.filter(f => !f.parentId),
      hasNextPage: false,
    };
  }

  async search(options: SearchOptions): Promise<ListResult> {
    const allFiles = generateDemoFiles(this.type);
    const query = options.query.toLowerCase();
    const filtered = allFiles.filter(
      f => f.name.toLowerCase().includes(query) || f.mimeType?.includes(query)
    );

    return {
      files: filtered,
      hasNextPage: false,
    };
  }

  async upload(options: UploadOptions): Promise<FileItem> {
    const path = options.path.endsWith('/') ? `${options.path}${options.file.name}` : `${options.path}/${options.file.name}`;
    const newFile: FileItem = {
      id: `upload-${Date.now()}`,
      name: options.file.name,
      path,
      size: options.file.size,
      mimeType: options.file.type,
      type: 'file',
      providerId: this.type,
      lastModified: new Date(),
      isStarred: false,
      isShared: false,
    };

    return newFile;
  }

  async download(_fileId: string): Promise<DownloadResult> {
    // Demo: return a dummy blob
    return {
      blob: new Blob(['Demo file content'], { type: 'application/octet-stream' }),
      fileName: 'demo-file.txt',
      mimeType: 'text/plain',
    };
  }

  async delete(_fileId: string): Promise<void> {
    // Demo: no-op
  }

  async getQuota(): Promise<StorageQuota> {
    return generateDemoQuota(this.type);
  }

  async refreshAccessToken?(_refreshToken: string): Promise<AuthResult> {
    return {
      success: true,
      accessToken: `refreshed-token-${Date.now()}`,
      expiresAt: new Date(Date.now() + 3600 * 1000),
    };
  }
}
