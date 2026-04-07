import { NextResponse } from "next/server";
import { RedditOrganicService } from "@/services/reddit/reddit-organic.service";

export async function POST() {
  try {
    const service = new RedditOrganicService();
    const summary = await service.syncAllTerms();
    return NextResponse.json(summary);
  } catch (err) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
