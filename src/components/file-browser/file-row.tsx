'use client';

import { type FileItem, getFileIcon, formatFileSize } from '@/lib/providers/types';
import { useCloudStore } from '@/lib/store';
import { FileIcon } from './file-icon';
import { Checkbox } from '@/components/ui/checkbox';
import { Star, Users } from 'lucide-react';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

interface FileRowProps {
  file: FileItem;
  index: number;
  onDoubleClick: () => void;
}

export function FileRow({ file, index, onDoubleClick }: FileRowProps) {
  const { selectedFiles, toggleFileSelection } = useCloudStore();
  const isSelected = selectedFiles.has(file.id);
  const iconType = getFileIcon(file.mimeType, file.name);
  const dateStr = new Date(file.lastModified).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });

  return (
    <motion.tr
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.15, delay: Math.min(index * 0.02, 0.2) }}
      className={cn(
        'group cursor-pointer transition-colors border-b border-border/30',
        'hover:bg-muted/60',
        isSelected && 'bg-primary/5'
      )}
      onClick={(e) => {
        if (e.ctrlKey || e.metaKey) {
          toggleFileSelection(file.id);
        } else {
          onDoubleClick();
        }
      }}
      onDoubleClick={onDoubleClick}
    >
      <td className="w-10 pl-4 py-2.5">
        <Checkbox
          checked={isSelected}
          onClick={(e) => {
            e.stopPropagation();
            toggleFileSelection(file.id);
          }}
          className="h-3.5 w-3.5"
        />
      </td>
      <td className="py-2.5">
        <div className="flex items-center gap-3 min-w-0">
          <FileIcon type={file.type === 'folder' ? 'folder' : iconType} size={32} />
          <div className="flex items-center gap-2 min-w-0">
            <span className="text-sm font-medium truncate">{file.name}</span>
            {file.isStarred && <Star className="h-3 w-3 text-amber-500 fill-amber-500 shrink-0" />}
            {file.isShared && <Users className="h-3 w-3 text-primary shrink-0" />}
          </div>
        </div>
      </td>
      <td className="py-2.5 text-sm text-muted-foreground">
        {file.type === 'folder' ? '—' : formatFileSize(file.size)}
      </td>
      <td className="py-2.5 text-sm text-muted-foreground hidden sm:table-cell">
        {dateStr}
      </td>
      <td className="py-2.5 text-sm text-muted-foreground hidden md:table-cell">
        {file.type === 'folder' ? 'Folder' : (file.mimeType?.split('/')[1]?.toUpperCase() || 'File')}
      </td>
    </motion.tr>
  );
}
