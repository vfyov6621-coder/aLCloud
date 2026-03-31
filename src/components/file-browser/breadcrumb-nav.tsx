'use client';

import { useCloudStore } from '@/lib/store';
import { ChevronRight, Home } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

export function BreadcrumbNav() {
  const { currentPath, navigateTo, selectedProvider } = useCloudStore();

  if (!selectedProvider) return null;

  const breadcrumbs = [
    { label: 'Home', path: [] },
    ...currentPath.map((segment, index) => ({
      label: segment,
      path: currentPath.slice(0, index + 1),
    })),
  ];

  return (
    <nav className="flex items-center gap-0.5 px-1 overflow-x-auto text-sm" aria-label="Breadcrumb">
      {breadcrumbs.map((crumb, index) => {
        const isLast = index === breadcrumbs.length - 1;

        return (
          <div key={crumb.path.join('/')} className="flex items-center">
            {index > 0 && (
              <ChevronRight className="h-3.5 w-3.5 text-muted-foreground/40 mx-1 shrink-0" />
            )}
            <Button
              variant="ghost"
              size="sm"
              className={cn(
                'h-7 px-2 text-sm font-normal',
                isLast
                  ? 'text-foreground font-medium'
                  : 'text-muted-foreground hover:text-foreground hover:bg-muted'
              )}
              onClick={() => !isLast && navigateTo(crumb.path)}
              disabled={isLast}
            >
              {index === 0 && <Home className="h-3.5 w-3.5 mr-1.5" />}
              {crumb.label}
            </Button>
          </div>
        );
      })}
    </nav>
  );
}
