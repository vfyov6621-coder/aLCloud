import { NextResponse } from 'next/server';

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ providerId: string }> }
) {
  const { providerId } = await params;

  // Demo OAuth - in production, this would redirect to the real OAuth provider
  const redirectUrl = `${process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'}/api/providers/${providerId}/callback?code=demo-auth-code-${Date.now()}`;

  return NextResponse.json({
    authUrl: redirectUrl,
    message: `In production, this would redirect to ${providerId}'s OAuth consent screen.`,
    providerId,
  });
}
