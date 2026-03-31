'use client';

import { useCallback } from 'react';
import { useCloudStore, type SortField } from '@/lib/store';
import { BreadcrumbNav } from './breadcrumb-nav';
import { FileGrid, FileList } from './file-grid';
import { EmptyState } from './empty-state';
import { UploadZone } from './upload-zone';
import { Button } from '@/components/ui/button';
import {
  LayoutGrid,
  List,
  ArrowUp,
  ArrowDown,
  Plus,
  CheckSquare,
  XCircle,
} from 'lucide-react';
import { cn } from '@/lib/utils';

function SortButton({ field, label, sortField, sortDirection, onSort }: {
  field: SortField;
  label: string;
  sortField: SortField;
  sortDirection: string;
  onSort: (field: SortField) => void;
}) {
  return (
    <button
      onClick={() => onSort(field)}
      className={cn(
        'flex items-center gap-1 px-2 py-1 rounded text-xs transition-colors',
        sortField === field
          ? 'text-foreground bg-muted font-medium'
          : 'text-muted-foreground hover:text-foreground hover:bg-muted/50'
      )}
    >
      {label}
      {sortField === field && (
        sortDirection === 'asc' ? <ArrowUp className="h-3 w-3" /> : <ArrowDown className="h-3 w-3" />
      )}
    </button>
  );
}

export function FileBrowser() {
  const {
    viewMode,
    sortField,
    sortDirection,
    selectedProvider,
    selectedFiles,
    loading,
    searchQuery,
    setViewMode,
    setSortField,
    setSortDirection,
    selectAll,
    clearSelection,
    setShowConnectDialog,
    getFilteredFiles,
  } = useCloudStore();

  const files = getFilteredFiles();
  const hasProviders = selectedProvider !== null;
  const isSearching = searchQuery.length > 0;
  const hasSelection = selectedFiles.size > 0;

  const handleSort = useCallback((field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  }, [sortField, sortDirection, setSortField, setSortDirection]);

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden">
      {/* Toolbar */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-border/50 shrink-0">
        <div className="flex items-center gap-2 min-w-0">
          <BreadcrumbNav />
        </div>

        <div className="flex items-center gap-1 shrink-0">
          {/* Sort controls */}
          <div className="hidden sm:flex items-center gap-0.5 mr-2">
            <SortButton field="name" label="Name" sortField={sortField} sortDirection={sortDirection} onSort={handleSort} />
            <SortButton field="size" label="Size" sortField={sortField} sortDirection={sortDirection} onSort={handleSort} />
            <SortButton field="date" label="Date" sortField={sortField} sortDirection={sortDirection} onSort={handleSort} />
            <SortButton field="type" label="Type" sortField={sortField} sortDirection={sortDirection} onSort={handleSort} />
          </div>

          {/* Select all */}
          {files.length > 0 && (
            <Button
              variant="ghost"
              size="icon"
              className="h-8 w-8"
              onClick={hasSelection ? clearSelection : selectAll}
              title={hasSelection ? 'Clear selection' : 'Select all'}
            >
              {hasSelection ? (
                <XCircle className="h-4 w-4" />
              ) : (
                <CheckSquare className="h-4 w-4" />
              )}
            </Button>
          )}

          {/* Selection count */}
          {hasSelection && (
            <span className="text-xs text-muted-foreground px-1.5 py-0.5 bg-muted rounded">
              {selectedFiles.size} selected
            </span>
          )}

          {/* View mode toggle */}
          <div className="flex items-center bg-muted/50 rounded-lg p-0.5">
            <Button
              variant={viewMode === 'grid' ? 'secondary' : 'ghost'}
              size="icon"
              className={cn('h-7 w-7', viewMode === 'grid' && 'shadow-sm')}
              onClick={() => setViewMode('grid')}
            >
              <LayoutGrid className="h-3.5 w-3.5" />
            </Button>
            <Button
              variant={viewMode === 'list' ? 'secondary' : 'ghost'}
              size="icon"
              className={cn('h-7 w-7', viewMode === 'list' && 'shadow-sm')}
              onClick={() => setViewMode('list')}
            >
              <List className="h-3.5 w-3.5" />
            </Button>
          </div>

          {/* Upload button */}
          {hasProviders && (
            <Button
              variant="default"
              size="sm"
              className="ml-1 h-8 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white shadow-sm"
              onClick={() => {
                const input = document.getElementById('file-upload');
                input?.click();
              }}
            >
              <Plus className="h-3.5 w-3.5 mr-1" />
              Upload
            </Button>
          )}
        </div>
      </div>

      {/* File content */}
      <div className="flex-1 overflow-auto relative">
        <UploadZone />

        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="flex flex-col items-center gap-3">
              <div className="w-8 h-8 border-2 border-primary/30 border-t-primary rounded-full animate-spin" />
              <p className="text-sm text-muted-foreground">Loading files...</p>
            </div>
          </div>
        ) : files.length > 0 ? (
          <div className="p-4 pt-2">
            {viewMode === 'grid' ? (
              <FileGrid />
            ) : (
              <FileList />
            )}
          </div>
        ) : (
          <EmptyState
            hasProviders={hasProviders}
            isSearching={isSearching}
            onConnect={() => setShowConnectDialog(true)}
            onUpload={() => {
              const input = document.getElementById('file-upload');
              input?.click();
            }}
          />
        )}
      </div>
    </div>
  );
}
