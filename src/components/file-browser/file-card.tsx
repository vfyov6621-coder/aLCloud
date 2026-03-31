'use client';

import { type FileItem, getFileIcon, formatFileSize } from '@/lib/providers/types';
import { useCloudStore } from '@/lib/store';
import { FileIcon } from './file-icon';
import { Checkbox } from '@/components/ui/checkbox';
import { Star, Users, MoreVertical } from 'lucide-react';
import { cn } from '@/lib/utils';
import { ContextMenu, ContextMenuContent, ContextMenuItem, ContextMenuTrigger, ContextMenuSeparator } from '@/components/ui/context-menu';
import { useState, useRef } from 'react';
import { motion } from 'framer-motion';

interface FileCardProps {
  file: FileItem;
  index: number;
  onDoubleClick: () => void;
}

export function FileCard({ file, index, onDoubleClick }: FileCardProps) {
  const { selectedFiles, toggleFileSelection, deleteFile, setShowFileInfo, selectedProvider } = useCloudStore();
  const isSelected = selectedFiles.has(file.id);
  const iconType = getFileIcon(file.mimeType, file.name);
  const [isDragOver, setIsDragOver] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  return (
    <ContextMenu>
      <ContextMenuTrigger>
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.2, delay: Math.min(index * 0.03, 0.3) }}
          className={cn(
            'group relative flex flex-col items-center p-3 rounded-xl cursor-pointer transition-all duration-150',
            'hover:bg-muted/80 border border-transparent',
            isSelected && 'bg-primary/5 border-primary/20 ring-1 ring-primary/20',
            isDragOver && 'bg-primary/10 border-primary/30'
          )}
          onClick={(e) => {
            if (e.ctrlKey || e.metaKey) {
              toggleFileSelection(file.id);
            } else {
              onDoubleClick();
            }
          }}
          onDoubleClick={onDoubleClick}
          onContextMenu={() => {}}
        >
          {/* Selection checkbox */}
          <div
            className={cn(
              'absolute top-2 left-2 z-10 opacity-0 group-hover:opacity-100 transition-opacity',
              isSelected && 'opacity-100'
            )}
            onClick={(e) => {
              e.stopPropagation();
              toggleFileSelection(file.id);
            }}
          >
            <Checkbox
              checked={isSelected}
              className="h-4 w-4 border-border/50"
            />
          </div>

          {/* File icon/thumbnail */}
          <div className="relative mb-2 w-16 h-16 flex items-center justify-center">
            <FileIcon type={file.type === 'folder' ? 'folder' : iconType} size={48} className="transition-transform group-hover:scale-105" />
            {file.isStarred && (
              <Star className="absolute -top-0.5 -right-0.5 h-3.5 w-3.5 text-amber-500 fill-amber-500" />
            )}
            {file.isShared && (
              <Users className="absolute -bottom-0.5 -right-0.5 h-3.5 w-3.5 text-primary" />
            )}
          </div>

          {/* File name */}
          <div className="w-full text-center">
            <p className="text-xs font-medium truncate text-foreground leading-tight" title={file.name}>
              {file.name}
            </p>
            {file.type === 'file' && (
              <p className="text-[10px] text-muted-foreground mt-0.5">
                {formatFileSize(file.size)}
              </p>
            )}
          </div>
        </motion.div>
      </ContextMenuTrigger>
      <ContextMenuContent className="w-48">
        <ContextMenuItem onClick={onDoubleClick}>
          {file.type === 'folder' ? 'Open' : 'Preview'}
        </ContextMenuItem>
        <ContextMenuItem onClick={() => {
          window.open(`/api/providers/${selectedProvider}/download/${file.id}`, '_blank');
        }}>
          Download
        </ContextMenuItem>
        <ContextMenuItem onClick={() => setShowFileInfo(file)}>
          Info
        </ContextMenuItem>
        <ContextMenuItem>
          {file.isStarred ? 'Unstar' : 'Star'}
        </ContextMenuItem>
        <ContextMenuSeparator />
        <ContextMenuItem className="text-destructive focus:text-destructive" onClick={() => deleteFile(file.id)}>
          Delete
        </ContextMenuItem>
      </ContextMenuContent>
    </ContextMenu>
  );
}
