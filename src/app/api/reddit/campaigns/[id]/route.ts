import { NextRequest, NextResponse } from "next/server";
import { RedditAdsService } from "@/services/reddit/reddit-ads.service";

interface UpdatePayload {
  action: "pause" | "activate" | "update";
  updates?: { name?: string; dailyBudgetAmount?: number };
}

export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const campaignId = params.id;
  if (!campaignId) {
    return NextResponse.json({ error: "Campaign ID is required" }, { status: 400 });
  }

  let body: UpdatePayload;
  try {
    body = (await request.json()) as UpdatePayload;
  } catch {
    return NextResponse.json({ error: "Invalid JSON body" }, { status: 400 });
  }

  const { action, updates } = body;
  if (!action || !["pause", "activate", "update"].includes(action)) {
    return NextResponse.json(
      { error: "action must be one of: pause, activate, update" },
      { status: 400 }
    );
  }

  try {
    const service = new RedditAdsService();
    let result;

    if (action === "pause") {
      result = await service.pauseCampaign(campaignId);
    } else if (action === "activate") {
      result = await service.activateCampaign(campaignId);
    } else {
      result = await service.updateCampaign(campaignId, updates ?? {});
    }

    return NextResponse.json({ success: true, campaign: result });
  } catch (err) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ success: false, error: message }, { status: 500 });
  }
}
