import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { redditTrackedTerms, redditMentions } from "@/lib/db/schema";
import { eq } from "drizzle-orm";

export async function DELETE(
  _request: NextRequest,
  { params }: { params: { id: string } }
) {
  const id = parseInt(params.id, 10);
  if (isNaN(id)) {
    return NextResponse.json({ error: "Invalid term ID" }, { status: 400 });
  }

  try {
    const [existing] = await db
      .select()
      .from(redditTrackedTerms)
      .where(eq(redditTrackedTerms.id, id));

    if (!existing) {
      return NextResponse.json({ error: "Term not found" }, { status: 404 });
    }

    // Remove associated mentions first, then the term
    await db.delete(redditMentions).where(eq(redditMentions.term, existing.term));
    await db.delete(redditTrackedTerms).where(eq(redditTrackedTerms.id, id));

    return NextResponse.json({ success: true, deleted: existing.term });
  } catch (err) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
