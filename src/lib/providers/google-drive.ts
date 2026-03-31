// Google Drive provider implementation
import { ProviderType, type ProviderInfo } from './types';
import { BaseProvider } from './base-provider';

export class GoogleDriveProvider extends BaseProvider {
  readonly type = ProviderType.GOOGLE_DRIVE;
  readonly info: ProviderInfo = {
    type: ProviderType.GOOGLE_DRIVE,
    name: 'Google Drive',
    description: 'Access your Google Drive files and folders',
    icon: 'google-drive',
    color: '#4285F4',
  };

  getAuthUrl(): string {
    // In production, this would construct a proper Google OAuth URL
    return `/api/providers/google-drive/auth`;
  }
}
