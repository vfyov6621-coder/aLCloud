// Yandex.Disk provider implementation
import { ProviderType, type ProviderInfo } from './types';
import { BaseProvider } from './base-provider';

export class YandexDiskProvider extends BaseProvider {
  readonly type = ProviderType.YANDEX_DISK;
  readonly info: ProviderInfo = {
    type: ProviderType.YANDEX_DISK,
    name: 'Yandex.Disk',
    description: 'Access your Yandex.Disk cloud storage',
    icon: 'yandex-disk',
    color: '#FC3F1D',
  };

  getAuthUrl(): string {
    return `/api/providers/yandex-disk/auth`;
  }
}
