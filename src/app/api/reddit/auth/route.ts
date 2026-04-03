import { NextResponse } from "next/server";
import { RedditAuthService } from "@/services/reddit/reddit-auth.service";
import crypto from "crypto";

export async function GET(): Promise<NextResponse> {
  try {
    const authService = new RedditAuthService();
    const state = crypto.randomBytes(16).toString("hex");
    const url = authService.getAuthUrl(state);
    return NextResponse.redirect(url);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
