// Mail.ru Cloud provider implementation
import { ProviderType, type ProviderInfo } from './types';
import { BaseProvider } from './base-provider';

export class MailRuCloudProvider extends BaseProvider {
  readonly type = ProviderType.MAILRU_CLOUD;
  readonly info: ProviderInfo = {
    type: ProviderType.MAILRU_CLOUD,
    name: 'Mail.ru Cloud',
    description: 'Access your Mail.ru Cloud storage',
    icon: 'mail-ru',
    color: '#005FF9',
  };

  getAuthUrl(): string {
    return `/api/providers/mailru-cloud/auth`;
  }
}
