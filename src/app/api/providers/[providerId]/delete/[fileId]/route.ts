import { NextResponse } from 'next/server';
import { getProvider } from '@/lib/providers';

export async function DELETE(
  _request: Request,
  { params }: { params: Promise<{ providerId: string; fileId: string }> }
) {
  const { providerId, fileId } = await params;

  try {
    const provider = getProvider(providerId);
    await provider.delete(fileId);

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Delete failed:', error);
    return NextResponse.json(
      { error: 'Delete failed' },
      { status: 500 }
    );
  }
}
