// Provider registry - provides access to all provider implementations
import { ProviderType, type IProvider, PROVIDERS_INFO } from './types';
import { GoogleDriveProvider } from './google-drive';
import { TelegramProvider } from './telegram';
import { YandexDiskProvider } from './yandex-disk';
import { MailRuCloudProvider } from './mailru-cloud';
import { GitHubProvider } from './github';

const providerInstances: Map<ProviderType, IProvider> = new Map();

function getProviderInstance(type: ProviderType): IProvider {
  if (!providerInstances.has(type)) {
    let provider: IProvider;
    switch (type) {
      case ProviderType.GOOGLE_DRIVE:
        provider = new GoogleDriveProvider();
        break;
      case ProviderType.TELEGRAM:
        provider = new TelegramProvider();
        break;
      case ProviderType.YANDEX_DISK:
        provider = new YandexDiskProvider();
        break;
      case ProviderType.MAILRU_CLOUD:
        provider = new MailRuCloudProvider();
        break;
      case ProviderType.GITHUB:
        provider = new GitHubProvider();
        break;
      default:
        throw new Error(`Unknown provider type: ${type}`);
    }
    providerInstances.set(type, provider);
  }
  return providerInstances.get(type)!;
}

export function getProvider(type: string): IProvider {
  return getProviderInstance(type as ProviderType);
}

export function getAllProviders(): IProvider[] {
  return Object.values(ProviderType).map(t => getProviderInstance(t));
}

export function getProviderInfo(type: string) {
  return PROVIDERS_INFO[type as ProviderType];
}

export { ProviderType, PROVIDERS_INFO };
export type { IProvider, ProviderInfo, FileItem, StorageQuota, AuthResult, ListResult } from './types';
