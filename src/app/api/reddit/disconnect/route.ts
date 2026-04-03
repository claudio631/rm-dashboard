import { NextResponse } from "next/server";
import { RedditAuthService } from "@/services/reddit/reddit-auth.service";

export async function POST(): Promise<NextResponse> {
  try {
    const authService = new RedditAuthService();
    await authService.clearTokens();
    return NextResponse.redirect("/settings/integrations?reddit=disconnected");
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
