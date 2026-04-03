import { NextRequest, NextResponse } from "next/server";
import { RedditAuthService } from "@/services/reddit/reddit-auth.service";

export async function GET(request: NextRequest): Promise<NextResponse> {
  const { searchParams } = new URL(request.url);
  const code = searchParams.get("code");
  const error = searchParams.get("error");

  if (error) {
    return NextResponse.redirect(
      `/settings/integrations?reddit=error&reason=${encodeURIComponent(error)}`
    );
  }

  if (!code) {
    return NextResponse.json({ error: "Missing authorization code" }, { status: 400 });
  }

  try {
    const authService = new RedditAuthService();
    await authService.exchangeCode(code);
    return NextResponse.redirect("/settings/integrations?reddit=connected");
  } catch (err) {
    const message = err instanceof Error ? err.message : "Token exchange failed";
    return NextResponse.redirect(
      `/settings/integrations?reddit=error&reason=${encodeURIComponent(message)}`
    );
  }
}
