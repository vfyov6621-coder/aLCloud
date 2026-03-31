'use client';

import { PROVIDERS_INFO, type ProviderType } from '@/lib/providers/types';

interface ProviderIconProps {
  providerType: string;
  size?: number;
  className?: string;
}

export function ProviderIcon({ providerType, size = 20, className = '' }: ProviderIconProps) {
  const info = PROVIDERS_INFO[providerType as ProviderType];
  const color = info?.color || '#888';

  switch (providerType) {
    case 'google-drive':
      return (
        <svg width={size} height={size} viewBox="0 0 24 24" className={className}>
          <path d="M7.71 3.5L1.15 15l3.43 6 6.57-11.5L7.71 3.5zm1.14 0L19.85 21H12.85L6.29 9.5l2.56-6z" fill={color} opacity="0.9"/>
          <path d="M12.86 10.5l3.57 6H9.29l3.57-6z" fill={color} opacity="0.7"/>
          <path d="M7.71 3.5l6.57 11.5h3.57L11.29 3.5H7.71z" fill={color} opacity="0.8"/>
        </svg>
      );
    case 'telegram':
      return (
        <svg width={size} height={size} viewBox="0 0 24 24" className={className}>
          <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.479.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z" fill={color}/>
        </svg>
      );
    case 'yandex-disk':
      return (
        <svg width={size} height={size} viewBox="0 0 24 24" className={className}>
          <rect x="2" y="2" width="20" height="20" rx="4" fill={color}/>
          <path d="M12 6c-2 0-3.5 1.2-3.5 3s1.2 2.5 2 3c-.8.5-2.5 1.2-2.5 3.2s1.8 2.8 4 2.8c2.5 0 4-1.3 4-2.8 0-2-1.7-2.7-2.5-3.2.8-.5 2-1.2 2-3S14 6 12 6zm0 5.5c-.7 0-1.5-.5-1.5-1.5S11.3 8.5 12 8.5s1.5.5 1.5 1.5S12.7 11.5 12 11.5zm0 6c-1 0-2-.5-2-1.5s1-1.5 2-1.5 2 .5 2 1.5-1 1.5-2 1.5z" fill="white"/>
        </svg>
      );
    case 'mailru-cloud':
      return (
        <svg width={size} height={size} viewBox="0 0 24 24" className={className}>
          <rect x="2" y="2" width="20" height="20" rx="4" fill={color}/>
          <path d="M8 8h8v2H8V8zm0 3h8v2H8v-2zm0 3h5v2H8v-2z" fill="white"/>
          <path d="M18 14l-3 3 1.5 1.5L21 14.5 16.5 10 15 11.5 18 14z" fill="white" opacity="0.7"/>
        </svg>
      );
    case 'github':
      return (
        <svg width={size} height={size} viewBox="0 0 24 24" className={className}>
          <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" fill={color}/>
        </svg>
      );
    default:
      return (
        <svg width={size} height={size} viewBox="0 0 24 24" className={className}>
          <circle cx="12" cy="12" r="10" fill={color} opacity="0.2"/>
          <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8z" fill={color}/>
        </svg>
      );
  }
}
