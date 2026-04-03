import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { redditAdPerformance } from "@/lib/db/schema";
import { desc, gte, sql } from "drizzle-orm";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const days = parseInt(searchParams.get("days") ?? "30", 10);

  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - days);
  const cutoffDate = cutoff.toISOString().split("T")[0];

  const rows = await db
    .select()
    .from(redditAdPerformance)
    .where(gte(redditAdPerformance.date, cutoffDate))
    .orderBy(desc(redditAdPerformance.date));

  return NextResponse.json({ data: rows, days });
}
