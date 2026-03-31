'use client';

import { Progress } from '@/components/ui/progress';
import { ProviderIcon } from '@/components/provider/provider-icon';
import { type ConnectedProvider } from '@/lib/store';

interface StorageUsageProps {
  provider: ConnectedProvider;
}

export function StorageUsage({ provider }: StorageUsageProps) {
  const quota = provider.quota;
  if (!quota) return null;

  const percentage = quota.total > 0 ? Math.round((quota.used / quota.total) * 100) : 0;

  return (
    <div className="flex items-center gap-2.5 py-1.5 px-3">
      <ProviderIcon providerType={provider.providerType} size={16} />
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between text-xs mb-1">
          <span className="text-sidebar-foreground/60 truncate">{provider.displayName}</span>
          <span className="text-sidebar-foreground/40 shrink-0 ml-2">
            {quota.usedLabel} / {quota.totalLabel}
          </span>
        </div>
        <Progress
          value={percentage}
          className="h-1.5 bg-sidebar-border/50"
        />
      </div>
    </div>
  );
}
