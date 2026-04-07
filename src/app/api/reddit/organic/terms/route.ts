import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { redditTrackedTerms } from "@/lib/db/schema";

export async function POST(request: NextRequest) {
  let body: { term?: string };
  try {
    body = (await request.json()) as { term?: string };
  } catch {
    return NextResponse.json({ error: "Invalid JSON body" }, { status: 400 });
  }

  const term = body.term?.trim();
  if (!term) {
    return NextResponse.json({ error: "term is required and must not be empty" }, { status: 400 });
  }

  try {
    const createdAt = new Date().toISOString();
    const [created] = await db
      .insert(redditTrackedTerms)
      .values({ term, createdAt })
      .returning();

    return NextResponse.json({ term: created }, { status: 201 });
  } catch (err) {
    const message = err instanceof Error ? err.message : "Unknown error";
    if (message.includes("UNIQUE")) {
      return NextResponse.json({ error: `Term "${term}" is already tracked` }, { status: 409 });
    }
    return NextResponse.json({ error: message }, { status: 500 });
  }
}

export async function GET() {
  try {
    const terms = await db.select().from(redditTrackedTerms);
    return NextResponse.json({ terms });
  } catch (err) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
