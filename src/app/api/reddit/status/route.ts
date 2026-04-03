import { NextResponse } from "next/server";
import { RedditAuthService } from "@/services/reddit/reddit-auth.service";

export async function GET(): Promise<NextResponse> {
  try {
    const authService = new RedditAuthService();
    const tokens = await authService.getStoredTokens();

    if (!tokens) {
      return NextResponse.json({
        connected: false,
        scopes: [],
        expires_at: null,
      });
    }

    return NextResponse.json({
      connected: true,
      scopes: tokens.scope.split(" "),
      expires_at: tokens.expiresAt,
    });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
