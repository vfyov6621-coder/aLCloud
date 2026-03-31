'use client';

import { useCloudStore } from '@/lib/store';
import { FileCard } from './file-card';
import { FileRow } from './file-row';

export function FileGrid() {
  const { files, selectedProvider, navigateTo, currentPath } = useCloudStore();

  const handleDoubleClick = (file: typeof files[0]) => {
    if (file.type === 'folder') {
      const folderName = file.name;
      navigateTo([...currentPath, folderName]);
    }
  };

  if (files.length === 0) return null;

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 2xl:grid-cols-7 gap-1 p-2">
      {files.map((file, index) => (
        <FileCard
          key={file.id}
          file={file}
          index={index}
          onDoubleClick={() => handleDoubleClick(file)}
        />
      ))}
    </div>
  );
}

export function FileList() {
  const { files, navigateTo, currentPath } = useCloudStore();

  const handleDoubleClick = (file: typeof files[0]) => {
    if (file.type === 'folder') {
      navigateTo([...currentPath, file.name]);
    }
  };

  if (files.length === 0) return null;

  return (
    <div className="w-full">
      <table className="w-full">
        <thead>
          <tr className="border-b border-border/50 text-left">
            <th className="w-10 pl-4 py-2"></th>
            <th className="py-2 px-3 text-xs font-medium text-muted-foreground">Name</th>
            <th className="py-2 px-3 text-xs font-medium text-muted-foreground w-24">Size</th>
            <th className="py-2 px-3 text-xs font-medium text-muted-foreground w-32 hidden sm:table-cell">Modified</th>
            <th className="py-2 px-3 text-xs font-medium text-muted-foreground w-20 hidden md:table-cell">Type</th>
          </tr>
        </thead>
        <tbody>
          {files.map((file, index) => (
            <FileRow
              key={file.id}
              file={file}
              index={index}
              onDoubleClick={() => handleDoubleClick(file)}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
}
