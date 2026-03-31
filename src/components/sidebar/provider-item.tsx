'use client';

import { type ConnectedProvider } from '@/lib/store';
import { ProviderIcon } from '@/components/provider/provider-icon';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

interface ProviderItemProps {
  provider: ConnectedProvider;
  isSelected: boolean;
  onClick: () => void;
}

export function ProviderItem({ provider, isSelected, onClick }: ProviderItemProps) {
  return (
    <button
      onClick={onClick}
      className={cn(
        'flex items-center gap-3 w-full px-3 py-2.5 rounded-lg text-sm transition-all duration-150',
        'hover:bg-sidebar-accent/80',
        isSelected && 'bg-sidebar-accent text-sidebar-accent-foreground'
      )}
    >
      <div className="relative shrink-0">
        <ProviderIcon providerType={provider.providerType} size={22} />
        <span className="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 bg-emerald-500 rounded-full border-2 border-sidebar" />
      </div>
      <div className="flex-1 text-left min-w-0">
        <div className="font-medium truncate text-sidebar-foreground">
          {provider.displayName}
        </div>
        <div className="text-xs text-sidebar-foreground/50 truncate">
          {provider.accountEmail || 'Connected'}
        </div>
      </div>
      {isSelected && (
        <Badge variant="secondary" className="text-[10px] px-1.5 py-0 h-4 bg-emerald-500/15 text-emerald-400 border-emerald-500/20">
          Active
        </Badge>
      )}
    </button>
  );
}
