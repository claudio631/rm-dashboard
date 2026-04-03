import { RedditAuthService } from "@/services/reddit/reddit-auth.service";

interface RedditStatus {
  connected: boolean;
  scopes: string[];
  expires_at: string | null;
}

async function getRedditStatus(): Promise<RedditStatus> {
  try {
    const authService = new RedditAuthService();
    const tokens = await authService.getStoredTokens();
    if (!tokens) return { connected: false, scopes: [], expires_at: null };
    return {
      connected: true,
      scopes: tokens.scope.split(" "),
      expires_at: tokens.expiresAt,
    };
  } catch {
    return { connected: false, scopes: [], expires_at: null };
  }
}

export default async function IntegrationsPage() {
  const reddit = await getRedditStatus();

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Integrations</h1>

      <div className="max-w-2xl">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-orange-500 flex items-center justify-center text-white font-bold text-sm">
                R
              </div>
              <div>
                <h2 className="text-base font-semibold text-gray-900">Reddit Ads</h2>
                <p className="text-sm text-gray-500">
                  Pull campaign analytics, manage ads, and monitor subreddits
                </p>
              </div>
            </div>

            <span
              className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${
                reddit.connected
                  ? "bg-green-50 text-green-700"
                  : "bg-gray-100 text-gray-600"
              }`}
            >
              <span
                className={`w-1.5 h-1.5 rounded-full ${
                  reddit.connected ? "bg-green-500" : "bg-gray-400"
                }`}
              />
              {reddit.connected ? "Connected" : "Disconnected"}
            </span>
          </div>

          {reddit.connected && (
            <div className="mt-4 pt-4 border-t border-gray-100 space-y-2 text-sm text-gray-600">
              <div>
                <span className="font-medium">Scopes:</span>{" "}
                {reddit.scopes.join(", ")}
              </div>
              {reddit.expires_at && (
                <div>
                  <span className="font-medium">Token expires:</span>{" "}
                  {new Date(reddit.expires_at).toLocaleString()}
                </div>
              )}
            </div>
          )}

          <div className="mt-4 pt-4 border-t border-gray-100 flex gap-3">
            {reddit.connected ? (
              <form action="/api/reddit/disconnect" method="POST">
                <button
                  type="submit"
                  className="px-4 py-2 text-sm font-medium text-red-600 bg-white border border-red-200 rounded-md hover:bg-red-50 transition-colors"
                >
                  Disconnect
                </button>
              </form>
            ) : (
              <a
                href="/api/reddit/auth"
                className="px-4 py-2 text-sm font-medium text-white bg-orange-500 rounded-md hover:bg-orange-600 transition-colors"
              >
                Connect Reddit
              </a>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
