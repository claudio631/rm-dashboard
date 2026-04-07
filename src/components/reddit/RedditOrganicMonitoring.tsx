"use client";

import { useState } from "react";

interface TrackedTerm {
  id: number;
  term: string;
  createdAt: string;
}

interface Mention {
  id: number;
  term: string;
  postId: string;
  title: string;
  url: string;
  subreddit: string;
  score: number;
  numComments: number;
  createdUtc: number;
  syncedAt: string;
}

interface Props {
  initialTerms: TrackedTerm[];
  initialMentions: Mention[];
}

function relativeTime(utcSeconds: number): string {
  const diffMs = Date.now() - utcSeconds * 1000;
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  if (diffDays === 0) return "today";
  if (diffDays === 1) return "yesterday";
  return `${diffDays}d ago`;
}

export function RedditOrganicMonitoring({ initialTerms, initialMentions }: Props) {
  const [terms, setTerms] = useState<TrackedTerm[]>(initialTerms);
  const [mentions, setMentions] = useState<Mention[]>(initialMentions);
  const [newTerm, setNewTerm] = useState("");
  const [addError, setAddError] = useState<string | null>(null);
  const [isSyncing, setIsSyncing] = useState(false);
  const [isAdding, setIsAdding] = useState(false);

  async function handleAddTerm() {
    const trimmed = newTerm.trim();
    if (!trimmed) return;

    setIsAdding(true);
    setAddError(null);

    try {
      const res = await fetch("/api/reddit/organic/terms", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ term: trimmed }),
      });
      const data = (await res.json()) as { term?: TrackedTerm; error?: string };

      if (!res.ok || !data.term) {
        setAddError(data.error ?? "Failed to add term");
        return;
      }

      setTerms((prev) => [...prev, data.term!]);
      setNewTerm("");
    } finally {
      setIsAdding(false);
    }
  }

  async function handleDeleteTerm(id: number, term: string) {
    try {
      await fetch(`/api/reddit/organic/terms/${id}`, { method: "DELETE" });
      setTerms((prev) => prev.filter((t) => t.id !== id));
      setMentions((prev) => prev.filter((m) => m.term !== term));
    } catch {
      // silent — term stays in list
    }
  }

  async function handleSync() {
    setIsSyncing(true);
    try {
      const res = await fetch("/api/reddit/organic/sync", { method: "POST" });
      if (res.ok) {
        // Refresh mentions from API
        const mentionsRes = await fetch("/api/reddit/organic/mentions?days=30");
        if (mentionsRes.ok) {
          const data = (await mentionsRes.json()) as { mentions: Mention[] };
          setMentions(data.mentions ?? []);
        }
      }
    } finally {
      setIsSyncing(false);
    }
  }

  return (
    <div className="space-y-4">
      {/* Tracked Terms */}
      <div>
        <p className="text-xs text-gray-500 mb-2">
          Monitor Reddit for mentions of these terms.
        </p>
        <div className="flex gap-2 mb-3">
          <input
            type="text"
            value={newTerm}
            onChange={(e) => setNewTerm(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAddTerm()}
            placeholder="e.g. Indeed Flex"
            className="flex-1 px-3 py-1.5 text-sm border border-gray-200 rounded-md focus:outline-none focus:ring-1 focus:ring-orange-300"
          />
          <button
            onClick={handleAddTerm}
            disabled={isAdding || !newTerm.trim()}
            className="px-3 py-1.5 text-xs font-medium text-white bg-orange-500 rounded-md hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isAdding ? "Adding…" : "Add"}
          </button>
        </div>
        {addError && <p className="text-xs text-red-500 mb-2">{addError}</p>}

        {terms.length === 0 ? (
          <p className="text-sm text-gray-400 italic">No terms tracked yet.</p>
        ) : (
          <div className="flex flex-wrap gap-2">
            {terms.map((t) => (
              <span
                key={t.id}
                className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-orange-50 text-orange-700 text-xs rounded-full"
              >
                {t.term}
                <button
                  onClick={() => handleDeleteTerm(t.id, t.term)}
                  className="text-orange-400 hover:text-orange-600 leading-none"
                  aria-label={`Remove ${t.term}`}
                >
                  ×
                </button>
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Sync + Mentions */}
      {terms.length > 0 && (
        <div>
          <div className="flex items-center justify-between mb-3">
            <p className="text-xs font-medium text-gray-500">
              Recent Mentions ({mentions.length})
            </p>
            <button
              onClick={handleSync}
              disabled={isSyncing}
              className="px-3 py-1 text-xs font-medium text-orange-600 bg-white border border-orange-200 rounded-md hover:bg-orange-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isSyncing ? "Syncing…" : "Sync Now"}
            </button>
          </div>

          {mentions.length === 0 ? (
            <p className="text-sm text-gray-400 italic">No mentions found. Run a sync.</p>
          ) : (
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {mentions.slice(0, 20).map((m) => (
                <a
                  key={m.id}
                  href={m.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block p-2 rounded-md border border-gray-100 hover:border-orange-200 hover:bg-orange-50 transition-colors"
                >
                  <div className="flex items-start justify-between gap-2">
                    <p className="text-sm text-gray-900 font-medium line-clamp-2 flex-1">
                      {m.title}
                    </p>
                    <span className="text-xs text-gray-400 shrink-0 mt-0.5">
                      {relativeTime(m.createdUtc)}
                    </span>
                  </div>
                  <div className="flex items-center gap-3 mt-1 text-xs text-gray-500">
                    <span className="text-orange-600">r/{m.subreddit}</span>
                    <span>↑ {m.score}</span>
                    <span>{m.numComments} comments</span>
                  </div>
                </a>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
