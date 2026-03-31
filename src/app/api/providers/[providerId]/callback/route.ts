import { NextResponse } from 'next/server';
import { db } from '@/lib/db';
import { getProvider } from '@/lib/providers';
import { PROVIDERS_INFO, ProviderType } from '@/lib/providers/types';

export async function GET(
  request: Request,
  { params }: { params: Promise<{ providerId: string }> }
) {
  const { providerId } = await params;
  const { searchParams } = new URL(request.url);
  const authCode = searchParams.get('code');

  if (!authCode) {
    return NextResponse.json({ error: 'No auth code provided' }, { status: 400 });
  }

  try {
    const provider = getProvider(providerId);
    const authResult = await provider.authenticate(authCode);

    if (!authResult.success) {
      return NextResponse.json(
        { error: authResult.error || 'Authentication failed' },
        { status: 401 }
      );
    }

    const info = PROVIDERS_INFO[providerId as ProviderType];
    if (!info) {
      return NextResponse.json({ error: 'Unknown provider' }, { status: 400 });
    }

    // Upsert connection
    const existing = await db.providerConnection.findFirst({
      where: { providerType: providerId, isConnected: true },
    });

    if (existing) {
      await db.providerConnection.update({
        where: { id: existing.id },
        data: {
          accessToken: authResult.accessToken || null,
          refreshToken: authResult.refreshToken || null,
          tokenExpiresAt: authResult.expiresAt || null,
          accountEmail: authResult.accountEmail || null,
          accountName: authResult.accountName || null,
          avatarUrl: authResult.avatarUrl || null,
          isConnected: true,
        },
      });
    } else {
      await db.providerConnection.create({
        data: {
          providerType: providerId,
          displayName: info.name,
          accessToken: authResult.accessToken || null,
          refreshToken: authResult.refreshToken || null,
          tokenExpiresAt: authResult.expiresAt || null,
          accountEmail: authResult.accountEmail || null,
          accountName: authResult.accountName || null,
          avatarUrl: authResult.avatarUrl || null,
          isConnected: true,
        },
      });
    }

    // Create some demo files
    const listResult = await provider.list('/');
    for (const file of listResult.files) {
      await db.fileItem.upsert({
        where: { id: file.id },
        update: {
          name: file.name,
          path: file.path,
          parentId: file.parentId || null,
          size: file.size,
          mimeType: file.mimeType || null,
          type: file.type,
          providerFileId: file.providerFileId || null,
          lastModified: file.lastModified,
          isStarred: file.isStarred,
          isShared: file.isShared,
        },
        create: {
          id: file.id,
          name: file.name,
          path: file.path,
          parentId: file.parentId || null,
          size: file.size,
          mimeType: file.mimeType || null,
          type: file.type,
          providerId: providerId,
          providerFileId: file.providerFileId || null,
          lastModified: file.lastModified,
          isStarred: file.isStarred,
          isShared: file.isShared,
        },
      });
    }

    return NextResponse.json({
      success: true,
      message: `Successfully connected to ${info.name}`,
      provider: {
        type: providerId,
        name: info.name,
        accountEmail: authResult.accountEmail,
        accountName: authResult.accountName,
      },
    });
  } catch (error) {
    console.error('Auth callback error:', error);
    return NextResponse.json(
      { error: 'Authentication failed' },
      { status: 500 }
    );
  }
}
