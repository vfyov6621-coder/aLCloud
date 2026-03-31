import { NextResponse } from 'next/server';
import { getProvider } from '@/lib/providers';

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ providerId: string }> }
) {
  const { providerId } = await params;

  try {
    const provider = getProvider(providerId);
    const quota = await provider.getQuota();

    return NextResponse.json(quota);
  } catch (error) {
    console.error('Failed to get quota:', error);
    return NextResponse.json(
      { error: 'Failed to get quota' },
      { status: 500 }
    );
  }
}
