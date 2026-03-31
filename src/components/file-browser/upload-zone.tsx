'use client';

import { useCallback, useState } from 'react';
import { useCloudStore } from '@/lib/store';
import { X, FileUp } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

export function UploadZone() {
  const { uploading, uploadProgress, selectedProvider, setFiles, setLoading, setUploading, setUploadProgress } = useCloudStore();
  const [isDragOver, setIsDragOver] = useState(false);
  const [uploadFiles, setUploadFiles] = useState<File[]>([]);
  const [showDropzone, setShowDropzone] = useState(false);

  const handleUpload = useCallback(async (files: FileList | File[]) => {
    if (!selectedProvider) return;

    const fileList = Array.from(files);
    if (fileList.length === 0) return;

    setUploading(true);
    setUploadProgress(0);

    try {
      for (let i = 0; i < fileList.length; i++) {
        const file = fileList[i];
        const formData = new FormData();
        formData.append('file', file);

        const res = await fetch(`/api/providers/${selectedProvider}/upload`, {
          method: 'POST',
          body: formData,
        });

        if (!res.ok) throw new Error(`Upload failed for ${file.name}`);

        setUploadProgress(((i + 1) / fileList.length) * 100);
      }

      // Refresh file list
      const listRes = await fetch(`/api/providers/${selectedProvider}/files?path=/`);
      if (listRes.ok) {
        const data = await listRes.json();
        setFiles(data.files || []);
      }
    } catch (error) {
      console.error('Upload error:', error);
    } finally {
      setUploading(false);
      setUploadProgress(0);
      setShowDropzone(false);
    }
  }, [selectedProvider, setFiles, setUploading, setUploadProgress]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(true);
    setShowDropzone(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleUpload(e.dataTransfer.files);
    }
  }, [handleUpload]);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      handleUpload(e.target.files);
    }
  }, [handleUpload]);

  return (
    <>
      {/* Global drag overlay */}
      {isDragOver && (
        <div className="fixed inset-0 z-[100] bg-primary/5 backdrop-blur-sm flex items-center justify-center pointer-events-none">
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="w-96 h-64 rounded-2xl border-2 border-dashed border-primary bg-card shadow-2xl flex flex-col items-center justify-center gap-4 pointer-events-auto"
          >
            <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center">
              <FileUp className="w-8 h-8 text-primary" />
            </div>
            <div className="text-center">
              <p className="font-medium text-foreground">Drop files to upload</p>
              <p className="text-sm text-muted-foreground mt-1">
                Files will be uploaded to current location
              </p>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsDragOver(false)}
              className="absolute top-3 right-3 h-7 w-7 p-0"
            >
              <X className="h-4 w-4" />
            </Button>
          </motion.div>
        </div>
      )}

      {/* Upload progress indicator */}
      {uploading && (
        <div className="absolute bottom-4 right-4 z-50">
          <div className="flex items-center gap-3 px-4 py-3 rounded-xl bg-card border border-border shadow-lg">
            <div className="relative w-10 h-10">
              <svg className="w-10 h-10 -rotate-90" viewBox="0 0 36 36">
                <path
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="3"
                  className="text-muted/30"
                />
                <path
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="3"
                  strokeDasharray={`${uploadProgress}, 100`}
                  className="text-emerald-500 transition-all duration-300"
                />
              </svg>
              <span className="absolute inset-0 flex items-center justify-center text-[10px] font-medium">
                {Math.round(uploadProgress)}%
              </span>
            </div>
            <div>
              <p className="text-sm font-medium">Uploading...</p>
              <p className="text-xs text-muted-foreground">{Math.round(uploadProgress)}% complete</p>
            </div>
          </div>
        </div>
      )}

      {/* File content area that accepts drops */}
      <div
        className={cn(
          'flex-1 relative',
          isDragOver && 'ring-2 ring-primary/30 ring-inset rounded-lg'
        )}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        {/* Hidden file input */}
        <input
          type="file"
          id="file-upload"
          className="hidden"
          multiple
          onChange={handleFileInput}
        />
      </div>
    </>
  );
}
