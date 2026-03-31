'use client';

import { type FileItem } from '@/lib/providers/types';

interface FileIconProps {
  type: string;
  size?: number;
  className?: string;
}

const iconColors: Record<string, string> = {
  folder: 'text-amber-500',
  image: 'text-pink-500',
  video: 'text-purple-500',
  audio: 'text-orange-500',
  'file-text': 'text-blue-500',
  sheet: 'text-emerald-500',
  presentation: 'text-orange-500',
  code: 'text-teal-500',
  archive: 'text-amber-600',
  pdf: 'text-red-500',
  file: 'text-muted-foreground/40',
};

import {
  Folder,
  File,
  Image,
  Video,
  Music,
  FileText,
  FileSpreadsheet,
  Presentation,
  Code,
  Archive,
  FileType,
} from 'lucide-react';

export function FileIcon({ type, size = 48, className = '' }: FileIconProps) {
  const color = iconColors[type] || iconColors.file;

  const iconMap: Record<string, React.ElementType> = {
    folder: Folder,
    image: Image,
    video: Video,
    audio: Music,
    'file-text': FileText,
    sheet: FileSpreadsheet,
    presentation: Presentation,
    code: Code,
    archive: Archive,
    pdf: FileType,
    file: File,
  };

  const Icon = iconMap[type] || File;

  return (
    <div className={`${className}`}>
      <Icon
        size={size}
        className={color}
        strokeWidth={type === 'folder' ? 1.5 : 1.2}
      />
    </div>
  );
}
