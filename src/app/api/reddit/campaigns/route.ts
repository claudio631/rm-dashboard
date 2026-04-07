import { NextResponse } from "next/server";
import { db } from "@/lib/db";
import { redditCampaigns } from "@/lib/db/schema";
import { ne } from "drizzle-orm";

export async function GET() {
  try {
    const campaigns = await db
      .select()
      .from(redditCampaigns)
      .where(ne(redditCampaigns.id, "account_total"));

    return NextResponse.json({ campaigns });
  } catch (err) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
