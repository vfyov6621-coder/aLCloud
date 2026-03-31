'use client';

import { useCloudStore } from '@/lib/store';
import { ProviderItem } from './provider-item';
import { StorageUsage } from './storage-usage';
import { ThemeToggle } from '@/components/theme/theme-toggle';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import { Button } from '@/components/ui/button';
import {
  Cloud,
  Plus,
  Clock,
  Star,
  Users,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { useState, useEffect } from 'react';
import type { StorageQuota, ProviderType, PROVIDERS_INFO } from '@/lib/providers/types';
import { getProviderInfo } from '@/lib/providers';

interface SidebarProps {
  className?: string;
}

export function Sidebar({ className }: SidebarProps) {
  const {
    providers,
    selectedProvider,
    sidebarOpen,
    setSelectedProvider,
    setShowConnectDialog,
    toggleSidebar,
    setSidebarOpen,
    fetchFiles,
  } = useCloudStore();

  const [quotas, setQuotas] = useState<Record<string, StorageQuota>>({});

  // Fetch quotas for connected providers
  useEffect(() => {
    const fetchQuotas = async () => {
      const newQuotas: Record<string, StorageQuota> = {};
      for (const p of providers) {
        if (p.isConnected) {
          try {
            const res = await fetch(`/api/providers/${p.providerType}/quota`);
            if (res.ok) {
              newQuotas[p.providerType] = await res.json();
            }
          } catch {
            // ignore
          }
        }
      }
      if (Object.keys(newQuotas).length > 0) {
        setQuotas(prev => ({ ...prev, ...newQuotas }));
      }
    };
    fetchQuotas();
  }, [providers]);

  const connectedProviders = providers.filter(p => p.isConnected);
  const providersWithQuota = connectedProviders.map(p => ({
    ...p,
    quota: quotas[p.providerType] || p.quota || null,
  }));

  const handleProviderClick = (providerType: string) => {
    setSelectedProvider(providerType);
    fetchFiles();
  };

  const quickLinks = [
    { icon: Clock, label: 'Recent', count: 24 },
    { icon: Star, label: 'Starred', count: 8 },
    { icon: Users, label: 'Shared', count: 3 },
  ];

  return (
    <>
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          'fixed lg:relative z-50 h-full flex flex-col bg-sidebar text-sidebar-foreground transition-all duration-300 ease-in-out',
          'w-64 flex-shrink-0',
          sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0 lg:w-0 lg:overflow-hidden',
          className
        )}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 shrink-0">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg shadow-emerald-500/20">
              <Cloud className="h-4.5 w-4.5 text-white" />
            </div>
            {sidebarOpen && (
              <span className="font-semibold text-base tracking-tight">aLCloud</span>
            )}
          </div>
          <div className="flex items-center gap-1">
            <ThemeToggle />
            <Button
              variant="ghost"
              size="icon"
              className="h-7 w-7 text-sidebar-foreground/50 hover:text-sidebar-foreground hover:bg-sidebar-accent"
              onClick={toggleSidebar}
            >
              {sidebarOpen ? <ChevronLeft className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
            </Button>
          </div>
        </div>

        <Separator className="bg-sidebar-border/50" />

        {/* Content */}
        <ScrollArea className="flex-1">
          <div className="p-3 space-y-4">
            {/* Quick Access */}
            <div>
              <h3 className="text-[11px] font-semibold uppercase tracking-wider text-sidebar-foreground/40 px-3 mb-2">
                Quick Access
              </h3>
              <div className="space-y-0.5">
                {quickLinks.map((link) => (
                  <button
                    key={link.label}
                    className="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm text-sidebar-foreground/70 hover:text-sidebar-foreground hover:bg-sidebar-accent/60 transition-colors"
                  >
                    <link.icon className="h-4 w-4" />
                    <span className="flex-1 text-left">{link.label}</span>
                    <span className="text-xs text-sidebar-foreground/30">{link.count}</span>
                  </button>
                ))}
              </div>
            </div>

            <Separator className="bg-sidebar-border/30" />

            {/* Cloud Providers */}
            <div>
              <div className="flex items-center justify-between px-3 mb-2">
                <h3 className="text-[11px] font-semibold uppercase tracking-wider text-sidebar-foreground/40">
                  Cloud Providers
                </h3>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-6 w-6 text-sidebar-foreground/40 hover:text-emerald-400 hover:bg-sidebar-accent"
                  onClick={() => setShowConnectDialog(true)}
                >
                  <Plus className="h-3.5 w-3.5" />
                </Button>
              </div>

              <div className="space-y-0.5">
                {connectedProviders.length === 0 ? (
                  <div className="px-3 py-4 text-center">
                    <Cloud className="h-8 w-8 mx-auto mb-2 text-sidebar-foreground/15" />
                    <p className="text-xs text-sidebar-foreground/30">No providers connected</p>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="mt-2 text-emerald-400 hover:text-emerald-300 hover:bg-emerald-500/10 text-xs h-7"
                      onClick={() => setShowConnectDialog(true)}
                    >
                      <Plus className="h-3 w-3 mr-1" />
                      Connect Provider
                    </Button>
                  </div>
                ) : (
                  connectedProviders.map((provider) => (
                    <ProviderItem
                      key={provider.id}
                      provider={provider}
                      isSelected={selectedProvider === provider.providerType}
                      onClick={() => handleProviderClick(provider.providerType)}
                    />
                  ))
                )}
              </div>
            </div>

            <Separator className="bg-sidebar-border/30" />

            {/* Storage Usage */}
            {providersWithQuota.length > 0 && (
              <div>
                <h3 className="text-[11px] font-semibold uppercase tracking-wider text-sidebar-foreground/40 px-3 mb-2">
                  Storage
                </h3>
                <div className="space-y-1">
                  {providersWithQuota.map((provider) => (
                    <StorageUsage key={provider.id} provider={provider} />
                  ))}
                </div>
              </div>
            )}
          </div>
        </ScrollArea>

        {/* Footer */}
        <Separator className="bg-sidebar-border/50" />
        <div className="px-4 py-2.5 shrink-0">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-full bg-gradient-to-br from-teal-400 to-emerald-600 flex items-center justify-center text-[11px] font-semibold text-white">
              U
            </div>
            <div className="flex-1 min-w-0">
              <div className="text-xs font-medium text-sidebar-foreground truncate">Demo User</div>
              <div className="text-[10px] text-sidebar-foreground/40 truncate">user@alcloud.app</div>
            </div>
          </div>
        </div>
      </aside>

      {/* Toggle button when collapsed */}
      {!sidebarOpen && (
        <Button
          variant="ghost"
          size="icon"
          className="fixed top-3 left-3 z-30 h-8 w-8 bg-card/80 backdrop-blur border border-border/50 shadow-sm hover:bg-accent lg:flex hidden"
          onClick={toggleSidebar}
        >
          <ChevronRight className="h-4 w-4" />
        </Button>
      )}
    </>
  );
}
