// Telegram provider implementation
import { ProviderType, type ProviderInfo } from './types';
import { BaseProvider } from './base-provider';

export class TelegramProvider extends BaseProvider {
  readonly type = ProviderType.TELEGRAM;
  readonly info: ProviderInfo = {
    type: ProviderType.TELEGRAM,
    name: 'Telegram',
    description: 'Access files shared in your Telegram chats',
    icon: 'telegram',
    color: '#26A5E4',
  };

  getAuthUrl(): string {
    return `/api/providers/telegram/auth`;
  }
}
