import { NextResponse } from 'next/server';
import { getProvider } from '@/lib/providers';

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ providerId: string; fileId: string }> }
) {
  const { providerId, fileId } = await params;

  try {
    const provider = getProvider(providerId);
    const result = await provider.download(fileId);

    return new Response(result.blob, {
      headers: {
        'Content-Type': result.mimeType,
        'Content-Disposition': `attachment; filename="${result.fileName}"`,
      },
    });
  } catch (error) {
    console.error('Download failed:', error);
    return NextResponse.json(
      { error: 'Download failed' },
      { status: 500 }
    );
  }
}
