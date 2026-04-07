import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { redditMentions } from "@/lib/db/schema";
import { and, eq, gte, ne } from "drizzle-orm";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const termFilter = searchParams.get("term");
  const daysParam = searchParams.get("days");
  const includeNsfw = searchParams.get("include_nsfw") === "true";

  const days = daysParam ? parseInt(daysParam, 10) : 30;
  if (isNaN(days) || days <= 0) {
    return NextResponse.json({ error: "days must be a positive integer" }, { status: 400 });
  }

  const cutoffUtc = Math.floor(Date.now() / 1000) - days * 24 * 60 * 60;

  try {
    const conditions = [gte(redditMentions.createdUtc, cutoffUtc)];
    if (termFilter) conditions.push(eq(redditMentions.term, termFilter));
    if (!includeNsfw) conditions.push(ne(redditMentions.over18, true));

    const mentions = await db
      .select()
      .from(redditMentions)
      .where(and(...conditions))
      .orderBy(redditMentions.createdUtc);

    return NextResponse.json({ mentions, count: mentions.length });
  } catch (err) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
