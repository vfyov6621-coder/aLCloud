'use client';

import { useCloudStore } from '@/lib/store';
import { Sidebar } from '@/components/sidebar/sidebar';
import { FileBrowser } from '@/components/file-browser/file-browser';
import { ConnectDialog } from '@/components/provider/connect-dialog';
import { FileInfoPanel } from '@/components/file-info/file-info-panel';
import { SearchBar } from '@/components/search/search-bar';
import { Button } from '@/components/ui/button';
import { Cloud, Menu } from 'lucide-react';
import { useSyncExternalStore } from 'react';

// Use useSyncExternalStore for mounted state to avoid setState-in-effect
const emptySubscribe = () => () => {};
function useMounted() {
  return useSyncExternalStore(emptySubscribe, () => true, () => false);
}

export default function HomePage() {
  const mounted = useMounted();
  const {
    sidebarOpen,
    setSidebarOpen,
    setShowConnectDialog,
    providers,
    selectedProvider,
  } = useCloudStore();

  if (!mounted) {
    return (
      <div className="h-screen flex items-center justify-center bg-background">
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center animate-pulse">
            <Cloud className="w-5 h-5 text-white" />
          </div>
          <p className="text-sm text-muted-foreground">Loading aLCloud...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen flex overflow-hidden bg-background">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Header */}
        <header className="flex items-center justify-between px-4 py-2.5 border-b border-border/50 shrink-0 bg-background/80 backdrop-blur-sm">
          <div className="flex items-center gap-3">
            <Button
              variant="ghost"
              size="icon"
              className="h-8 w-8 lg:hidden"
              onClick={() => setSidebarOpen(!sidebarOpen)}
            >
              <Menu className="h-4 w-4" />
            </Button>
            <div className="hidden sm:block">
              <h1 className="text-sm font-medium text-foreground">
                {selectedProvider
                  ? `${providers.find(p => p.providerType === selectedProvider)?.displayName || 'Files'}`
                  : 'All Files'}
              </h1>
              <p className="text-[11px] text-muted-foreground">
                {selectedProvider
                  ? `${providers.filter(p => p.isConnected).length} providers connected`
                  : 'Connect a provider to get started'}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <SearchBar />
            <Button
              variant="outline"
              size="sm"
              className="h-8 text-xs gap-1.5 hidden sm:flex"
              onClick={() => setShowConnectDialog(true)}
            >
              <Cloud className="h-3.5 w-3.5" />
              Connect
            </Button>
          </div>
        </header>

        {/* File Browser */}
        <FileBrowser />
      </main>

      {/* Dialogs & Panels */}
      <ConnectDialog />
      <FileInfoPanel />
    </div>
  );
}
