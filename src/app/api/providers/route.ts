import { NextResponse } from 'next/server';
import { db } from '@/lib/db';
import { getProvider } from '@/lib/providers';
import { ProviderType } from '@/lib/providers/types';

export async function GET() {
  try {
    const connections = await db.providerConnection.findMany({
      where: { isConnected: true },
      orderBy: { createdAt: 'desc' },
    });

    const providers = await Promise.all(
      connections.map(async (conn) => {
        let quota = null;
        try {
          const provider = getProvider(conn.providerType);
          quota = await provider.getQuota();
        } catch {
          // quota unavailable
        }

        return {
          id: conn.id,
          providerType: conn.providerType,
          displayName: conn.displayName,
          isConnected: conn.isConnected,
          accountEmail: conn.accountEmail,
          accountName: conn.accountName,
          avatarUrl: conn.avatarUrl,
          quota,
        };
      })
    );

    // Also include available provider types for the UI
    const availableTypes = Object.values(ProviderType).map((type) => {
      const provider = getProvider(type);
      return provider.info;
    });

    return NextResponse.json({
      connected: providers,
      available: availableTypes,
    });
  } catch (error) {
    console.error('Failed to list providers:', error);
    return NextResponse.json(
      { error: 'Failed to list providers' },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { providerType, displayName, accountEmail, accountName } = body;

    if (!providerType || !displayName) {
      return NextResponse.json(
        { error: 'providerType and displayName are required' },
        { status: 400 }
      );
    }

    // Check if already connected
    const existing = await db.providerConnection.findFirst({
      where: { providerType, isConnected: true },
    });

    if (existing) {
      return NextResponse.json({
        id: existing.id,
        ...existing,
        message: 'Provider already connected',
      });
    }

    // Create connection
    const connection = await db.providerConnection.create({
      data: {
        providerType,
        displayName,
        isConnected: true,
        accountEmail: accountEmail || null,
        accountName: accountName || null,
        accessToken: `demo-token-${providerType}-${Date.now()}`,
      },
    });

    return NextResponse.json(connection);
  } catch (error) {
    console.error('Failed to connect provider:', error);
    return NextResponse.json(
      { error: 'Failed to connect provider' },
      { status: 500 }
    );
  }
}
