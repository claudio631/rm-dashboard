"use client";

import { useState } from "react";

interface Campaign {
  id: string;
  name: string;
  status: string;
  objective: string | null;
  dailyBudgetAmount: number | null;
  currency: string | null;
  syncedAt: string;
}

interface Props {
  initialCampaigns: Campaign[];
}

function StatusBadge({ status }: { status: string }) {
  const isActive = status.includes("ACTIVE");
  const isPaused = status.includes("PAUSED");

  const classes = isActive
    ? "bg-green-50 text-green-700"
    : isPaused
    ? "bg-yellow-50 text-yellow-700"
    : "bg-gray-100 text-gray-600";

  const label = isActive ? "Active" : isPaused ? "Paused" : status;

  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${classes}`}>
      {label}
    </span>
  );
}

export function RedditCampaignTable({ initialCampaigns }: Props) {
  const [campaigns, setCampaigns] = useState<Campaign[]>(initialCampaigns);
  const [loadingId, setLoadingId] = useState<string | null>(null);
  const [errorId, setErrorId] = useState<string | null>(null);

  if (campaigns.length === 0) {
    return (
      <p className="text-sm text-gray-500 italic">
        No campaigns found. Run a sync to pull campaign data.
      </p>
    );
  }

  async function handleAction(campaignId: string, action: "pause" | "activate") {
    setLoadingId(campaignId);
    setErrorId(null);

    try {
      const res = await fetch(`/api/reddit/campaigns/${campaignId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action }),
      });

      const data = (await res.json()) as { success: boolean; campaign?: Campaign; error?: string };

      if (!res.ok || !data.success) {
        setErrorId(campaignId);
        return;
      }

      if (data.campaign) {
        setCampaigns((prev) =>
          prev.map((c) =>
            c.id === campaignId ? { ...c, status: data.campaign!.status } : c
          )
        );
      }
    } catch {
      setErrorId(campaignId);
    } finally {
      setLoadingId(null);
    }
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-gray-100">
            <th className="text-left text-xs font-medium text-gray-500 pb-2 pr-4">Campaign</th>
            <th className="text-left text-xs font-medium text-gray-500 pb-2 pr-4">Status</th>
            <th className="text-left text-xs font-medium text-gray-500 pb-2">Action</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-50">
          {campaigns.map((campaign) => {
            const isLoading = loadingId === campaign.id;
            const hasError = errorId === campaign.id;
            const isActive = campaign.status.includes("ACTIVE");

            return (
              <tr key={campaign.id}>
                <td className="py-2 pr-4 text-gray-900 font-medium truncate max-w-[200px]">
                  {campaign.name}
                </td>
                <td className="py-2 pr-4">
                  <StatusBadge status={campaign.status} />
                </td>
                <td className="py-2">
                  <button
                    onClick={() => handleAction(campaign.id, isActive ? "pause" : "activate")}
                    disabled={isLoading}
                    className={`px-3 py-1 text-xs font-medium rounded border transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${
                      isActive
                        ? "text-yellow-700 border-yellow-200 bg-white hover:bg-yellow-50"
                        : "text-green-700 border-green-200 bg-white hover:bg-green-50"
                    }`}
                  >
                    {isLoading ? "Updating…" : isActive ? "Pause" : "Activate"}
                  </button>
                  {hasError && (
                    <span className="ml-2 text-xs text-red-500">Failed — try again</span>
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
