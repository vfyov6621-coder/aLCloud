import { NextResponse } from 'next/server';
import { getProvider } from '@/lib/providers';

export async function POST(
  request: Request,
  { params }: { params: Promise<{ providerId: string }> }
) {
  const { providerId } = await params;

  try {
    const formData = await request.formData();
    const file = formData.get('file') as File | null;
    const path = formData.get('path') as string | null;

    if (!file) {
      return NextResponse.json({ error: 'No file provided' }, { status: 400 });
    }

    const provider = getProvider(providerId);
    const result = await provider.upload({
      file,
      path: path || '/',
    });

    return NextResponse.json({
      success: true,
      file: {
        ...result,
        lastModified: result.lastModified instanceof Date ? result.lastModified.toISOString() : result.lastModified,
      },
    });
  } catch (error) {
    console.error('Upload failed:', error);
    return NextResponse.json(
      { error: 'Upload failed' },
      { status: 500 }
    );
  }
}
