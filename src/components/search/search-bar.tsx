'use client';

import { useCloudStore } from '@/lib/store';
import { Search, X } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { useCallback, useEffect, useState } from 'react';

export function SearchBar() {
  const { searchQuery, setSearchQuery, searchFiles } = useCloudStore();
  const [isOpen, setIsOpen] = useState(false);
  const [localQuery, setLocalQuery] = useState('');

  // Sync local query with store
  useEffect(() => {
    setLocalQuery(searchQuery);
  }, [searchQuery]);

  const handleSearch = useCallback(() => {
    if (localQuery !== searchQuery) {
      setSearchQuery(localQuery);
      searchFiles(localQuery);
    }
  }, [localQuery, searchQuery, setSearchQuery, searchFiles]);

  const handleClear = useCallback(() => {
    setLocalQuery('');
    setSearchQuery('');
    searchFiles('');
  }, [setSearchQuery, searchFiles]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
    if (e.key === 'Escape') {
      handleClear();
      setIsOpen(false);
    }
  }, [handleSearch, handleClear]);

  return (
    <div className="relative flex items-center">
      <div
        className={cn(
          'flex items-center transition-all duration-200',
          isOpen ? 'w-64' : 'w-9'
        )}
      >
        <Button
          variant="ghost"
          size="icon"
          className="h-9 w-9 shrink-0 text-muted-foreground hover:text-foreground"
          onClick={() => setIsOpen(!isOpen)}
        >
          <Search className="h-4 w-4" />
        </Button>

        {isOpen && (
          <div className="flex-1 relative animate-in slide-in-from-right-2 duration-150">
            <Input
              type="text"
              placeholder="Search files..."
              value={localQuery}
              onChange={(e) => setLocalQuery(e.target.value)}
              onKeyDown={handleKeyDown}
              className="h-9 text-sm pr-8 border-0 bg-muted/50 focus-visible:ring-1"
              autoFocus
            />
            {localQuery && (
              <Button
                variant="ghost"
                size="icon"
                className="absolute right-0 top-0 h-9 w-9 text-muted-foreground hover:text-foreground"
                onClick={handleClear}
              >
                <X className="h-3 w-3" />
              </Button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
