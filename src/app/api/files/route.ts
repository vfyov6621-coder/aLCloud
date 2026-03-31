import { NextResponse } from 'next/server';
import { getAllProviders } from '@/lib/providers';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const query = searchParams.get('query') || '';
  const provider = searchParams.get('provider') || undefined;

  if (!query) {
    return NextResponse.json({ files: [] });
  }

  try {
    let providers = getAllProviders();

    if (provider) {
      providers = providers.filter(p => p.type === provider);
    }

    const allFiles = await Promise.all(
      providers.map(async (p) => {
        try {
          const result = await p.search({ query });
          return result.files.map(f => ({
            ...f,
            lastModified: f.lastModified instanceof Date ? f.lastModified.toISOString() : f.lastModified,
          }));
        } catch {
          return [];
        }
      })
    );

    const files = allFiles.flat();

    return NextResponse.json({ files });
  } catch (error) {
    console.error('Search failed:', error);
    return NextResponse.json(
      { error: 'Search failed' },
      { status: 500 }
    );
  }
}
