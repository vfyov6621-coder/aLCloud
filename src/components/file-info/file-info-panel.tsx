'use client';

import { useCloudStore } from '@/lib/store';
import { formatFileSize, getFileIcon } from '@/lib/providers/types';
import { FileIcon } from '@/components/file-browser/file-icon';
import { Sheet, SheetContent, SheetHeader, SheetTitle } from '@/components/ui/sheet';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { PROVIDERS_INFO } from '@/lib/providers/types';
import {
  Download,
  Share2,
  Star,
  Trash2,
  ExternalLink,
  Calendar,
  HardDrive,
  FileIcon as FileIconLucide,
} from 'lucide-react';

export function FileInfoPanel() {
  const { showFileInfo, setShowFileInfo, deleteFile, selectedProvider } = useCloudStore();

  const file = showFileInfo;
  if (!file) return null;

  const providerInfo = PROVIDERS_INFO[file.providerId as keyof typeof PROVIDERS_INFO];
  const iconType = getFileIcon(file.mimeType, file.name);

  const handleDownload = () => {
    if (selectedProvider) {
      window.open(`/api/providers/${selectedProvider}/download/${file.id}`, '_blank');
    }
  };

  const handleDelete = () => {
    deleteFile(file.id);
  };

  const dateStr = new Date(file.lastModified).toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });

  return (
    <Sheet open={!!file} onOpenChange={(open) => !open && setShowFileInfo(null)}>
      <SheetContent className="w-80 sm:w-96 p-0">
        <SheetHeader className="px-6 py-4 border-b bg-muted/20">
          <SheetTitle className="text-sm">File Details</SheetTitle>
        </SheetHeader>

        <div className="p-6 space-y-5">
          {/* Preview / Icon */}
          <div className="flex justify-center py-4">
            <div className="w-24 h-24 rounded-2xl bg-muted/50 flex items-center justify-center">
              <FileIcon type={file.type === 'folder' ? 'folder' : iconType} size={52} />
            </div>
          </div>

          {/* File name */}
          <div className="text-center">
            <h3 className="font-medium text-base leading-tight">{file.name}</h3>
            <div className="flex items-center justify-center gap-2 mt-2">
              <Badge variant="outline" className="text-[10px]">
                {file.type === 'folder' ? 'Folder' : (file.mimeType?.split('/')[1] || 'File').toUpperCase()}
              </Badge>
              {providerInfo && (
                <Badge variant="outline" className="text-[10px]">
                  {providerInfo.name}
                </Badge>
              )}
            </div>
          </div>

          <Separator />

          {/* Details */}
          <div className="space-y-3">
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground flex items-center gap-2">
                <HardDrive className="h-3.5 w-3.5" />
                Size
              </span>
              <span className="font-medium">
                {file.type === 'folder' ? '—' : formatFileSize(file.size)}
              </span>
            </div>

            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground flex items-center gap-2">
                <Calendar className="h-3.5 w-3.5" />
                Modified
              </span>
              <span className="font-medium text-right max-w-[180px] truncate">
                {dateStr}
              </span>
            </div>

            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground flex items-center gap-2">
                <FileIconLucide className="h-3.5 w-3.5" />
                Type
              </span>
              <span className="font-medium">{file.mimeType || 'Unknown'}</span>
            </div>

            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground">Location</span>
              <span className="font-medium text-right max-w-[180px] truncate text-xs">
                {file.path}
              </span>
            </div>

            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground flex items-center gap-2">
                <Star className="h-3.5 w-3.5" />
                Starred
              </span>
              <span className="font-medium">{file.isStarred ? 'Yes' : 'No'}</span>
            </div>

            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground flex items-center gap-2">
                <Share2 className="h-3.5 w-3.5" />
                Shared
              </span>
              <span className="font-medium">{file.isShared ? 'Yes' : 'No'}</span>
            </div>
          </div>

          <Separator />

          {/* Actions */}
          <div className="space-y-2">
            <Button variant="outline" className="w-full justify-start gap-2" onClick={handleDownload}>
              <Download className="h-4 w-4" />
              Download
            </Button>
            <Button variant="outline" className="w-full justify-start gap-2">
              <Share2 className="h-4 w-4" />
              Share
            </Button>
            <Button variant="outline" className="w-full justify-start gap-2">
              <ExternalLink className="h-4 w-4" />
              Open in {providerInfo?.name}
            </Button>
            <Separator />
            <Button
              variant="destructive"
              className="w-full justify-start gap-2"
              onClick={handleDelete}
            >
              <Trash2 className="h-4 w-4" />
              Delete
            </Button>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
}
