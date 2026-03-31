'use client';

import { useState } from 'react';
import { useCloudStore } from '@/lib/store';
import { ProviderIcon } from '@/components/provider/provider-icon';
import { PROVIDERS_INFO, type ProviderType } from '@/lib/providers/types';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Check, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

export function ConnectDialog() {
  const { showConnectDialog, setShowConnectDialog, providers, connectProvider } = useCloudStore();
  const [connecting, setConnecting] = useState<string | null>(null);

  const connectedTypes = new Set(
    providers.filter(p => p.isConnected).map(p => p.providerType)
  );

  const providerList = Object.values(ProviderType);
  const availableProviders = providerList.filter(t => !connectedTypes.has(t));
  const allProviders = providerList;

  const handleConnect = async (type: ProviderType) => {
    setConnecting(type);
    
    // Simulate OAuth flow with delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Call API to "connect" (demo)
    try {
      const info = PROVIDERS_INFO[type];
      const res = await fetch('/api/providers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          providerType: type,
          displayName: info.name,
          accountEmail: `user@${info.name.toLowerCase().replace(/\s/g, '').replace('.', '')}.com`,
          accountName: 'Demo User',
        }),
      });
      const data = await res.json();
      
      // Also call the auth callback to seed demo data
      await fetch(`/api/providers/${type}/callback?code=demo-code-${Date.now()}`);
      
      connectProvider(type);
    } catch (err) {
      console.error('Connection error:', err);
    } finally {
      setConnecting(null);
    }
  };

  return (
    <Dialog open={showConnectDialog} onOpenChange={setShowConnectDialog}>
      <DialogContent className="sm:max-w-lg p-0 gap-0 overflow-hidden">
        <div className="bg-gradient-to-r from-emerald-600/10 to-teal-600/10 px-6 py-5 border-b">
          <DialogHeader>
            <DialogTitle className="text-lg">Connect Cloud Provider</DialogTitle>
            <DialogDescription>
              Choose a provider to connect and manage your files
            </DialogDescription>
          </DialogHeader>
        </div>

        <div className="px-4 py-3">
          {allProviders.map((type, index) => {
            const info = PROVIDERS_INFO[type];
            const isConnected = connectedTypes.has(type);
            const isConnecting = connecting === type;

            return (
              <motion.div
                key={type}
                initial={{ opacity: 0, y: 4 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
                className={cn(
                  'flex items-center gap-4 p-3 rounded-xl transition-all duration-150',
                  isConnected
                    ? 'bg-muted/40'
                    : 'hover:bg-muted/70 cursor-pointer',
                  index < allProviders.length - 1 && 'mb-1'
                )}
                onClick={() => !isConnected && !isConnecting && handleConnect(type)}
              >
                <div className="shrink-0">
                  <ProviderIcon providerType={type} size={28} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-sm">{info.name}</span>
                    {isConnected && (
                      <Badge variant="secondary" className="text-[10px] px-1.5 py-0 h-4 bg-emerald-500/15 text-emerald-500 border-emerald-500/20">
                        Connected
                      </Badge>
                    )}
                  </div>
                  <p className="text-xs text-muted-foreground mt-0.5 truncate">
                    {info.description}
                  </p>
                </div>
                <div className="shrink-0">
                  {isConnected ? (
                    <div className="w-8 h-8 rounded-full bg-emerald-500/10 flex items-center justify-center">
                      <Check className="h-4 w-4 text-emerald-500" />
                    </div>
                  ) : isConnecting ? (
                    <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                      <Loader2 className="h-4 w-4 text-primary animate-spin" />
                    </div>
                  ) : (
                    <Button size="sm" variant="outline" className="h-8 text-xs">
                      Connect
                    </Button>
                  )}
                </div>
              </motion.div>
            );
          })}
        </div>

        <div className="px-6 py-3 border-t bg-muted/20">
          <p className="text-[11px] text-muted-foreground text-center">
            By connecting, you authorize aLCloud to access your cloud storage. Your credentials are securely stored.
          </p>
        </div>
      </DialogContent>
    </Dialog>
  );
}
