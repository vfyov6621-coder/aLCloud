// GitHub provider implementation
import { ProviderType, type ProviderInfo } from './types';
import { BaseProvider } from './base-provider';

export class GitHubProvider extends BaseProvider {
  readonly type = ProviderType.GITHUB;
  readonly info: ProviderInfo = {
    type: ProviderType.GITHUB,
    name: 'GitHub',
    description: 'Access your GitHub repositories and releases',
    icon: 'github',
    color: '#6E40C9',
  };

  getAuthUrl(): string {
    return `/api/providers/github/auth`;
  }
}
