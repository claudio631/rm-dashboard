import { NextResponse } from "next/server";
import { RedditAdsService } from "@/services/reddit/reddit-ads.service";

export async function POST() {
  try {
    const service = new RedditAdsService();
    const summary = await service.syncLast30Days();
    return NextResponse.json(summary);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Sync failed";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
