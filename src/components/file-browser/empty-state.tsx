'use client';

import { Cloud, FolderOpen, ArrowUpFromLine } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface EmptyStateProps {
  hasProviders?: boolean;
  isSearching?: boolean;
  onConnect?: () => void;
  onUpload?: () => void;
}

export function EmptyState({ hasProviders = false, isSearching = false, onConnect, onUpload }: EmptyStateProps) {
  if (isSearching) {
    return (
      <div className="flex flex-col items-center justify-center py-20 px-4">
        <div className="w-20 h-20 rounded-2xl bg-muted/50 flex items-center justify-center mb-4">
          <svg className="w-10 h-10 text-muted-foreground/30" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.3-4.3" />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-foreground mb-1">No results found</h3>
        <p className="text-sm text-muted-foreground text-center max-w-sm">
          Try adjusting your search query or searching across all providers.
        </p>
      </div>
    );
  }

  if (!hasProviders) {
    return (
      <div className="flex flex-col items-center justify-center py-20 px-4">
        <div className="w-24 h-24 rounded-3xl bg-gradient-to-br from-emerald-500/10 to-teal-500/10 flex items-center justify-center mb-6 border border-emerald-500/10">
          <Cloud className="w-12 h-12 text-emerald-500/60" />
        </div>
        <h3 className="text-xl font-semibold text-foreground mb-2">Welcome to aLCloud</h3>
        <p className="text-sm text-muted-foreground text-center max-w-md mb-6 leading-relaxed">
          Connect your cloud storage providers to manage all your files in one unified interface.
          Supports Google Drive, Telegram, Yandex.Disk, Mail.ru Cloud, and GitHub.
        </p>
        <Button
          onClick={onConnect}
          className="bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white shadow-lg shadow-emerald-500/20"
        >
          Connect Your First Provider
        </Button>
        <div className="mt-8 grid grid-cols-5 gap-4 opacity-40">
          {['Google Drive', 'Telegram', 'Yandex.Disk', 'Mail.ru', 'GitHub'].map((name) => (
            <div key={name} className="text-center">
              <div className="w-10 h-10 mx-auto rounded-lg bg-muted flex items-center justify-center mb-1">
                <Cloud className="w-5 h-5 text-muted-foreground" />
              </div>
              <span className="text-[10px] text-muted-foreground">{name}</span>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center py-20 px-4">
      <div className="w-20 h-20 rounded-2xl bg-muted/50 flex items-center justify-center mb-4">
        <FolderOpen className="w-10 h-10 text-muted-foreground/30" />
      </div>
      <h3 className="text-lg font-medium text-foreground mb-1">This folder is empty</h3>
      <p className="text-sm text-muted-foreground text-center max-w-sm mb-4">
        Drag and drop files here, or click to upload.
      </p>
      <Button variant="outline" onClick={onUpload} className="gap-2">
        <ArrowUpFromLine className="h-4 w-4" />
        Upload Files
      </Button>
    </div>
  );
}
