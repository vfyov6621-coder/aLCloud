import { NextResponse } from 'next/server';
import { getProvider } from '@/lib/providers';

export async function GET(
  request: Request,
  { params }: { params: Promise<{ providerId: string }> }
) {
  const { providerId } = await params;
  const { searchParams } = new URL(request.url);
  const path = searchParams.get('path') || '/';
  const pageToken = searchParams.get('pageToken') || undefined;

  try {
    const provider = getProvider(providerId);
    const result = await provider.list(path, pageToken);

    return NextResponse.json({
      files: result.files.map(f => ({
        ...f,
        lastModified: f.lastModified instanceof Date ? f.lastModified.toISOString() : f.lastModified,
      })),
      hasNextPage: result.hasNextPage,
      nextCursor: result.nextCursor,
    });
  } catch (error) {
    console.error('Failed to list files:', error);
    return NextResponse.json(
      { error: 'Failed to list files' },
      { status: 500 }
    );
  }
}
