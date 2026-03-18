export default function HomePage() {
  return (
    <div className="space-y-8">
      <div className="text-center space-y-4 py-12">
        <h1 className="text-4xl font-bold tracking-tight">
          RM Team AI
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          AI-powered recruitment marketing analytics for Indeed Flex.
          Upload your FHS, Indeed, and Tableau reports — get instant
          funnel analysis, cost-per-stage metrics, and your daily Slack
          report in one click.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <QuickAction
          href="/upload"
          title="Upload Reports"
          description="Drop FHS, Indeed, and Tableau exports to start analysis"
          icon="📁"
        />
        <QuickAction
          href="/dashboard"
          title="Dashboard"
          description="7-stage funnel analytics by client and market"
          icon="📊"
        />
        <QuickAction
          href="/tools/utm-builder"
          title="Tools"
          description="UTM builder, ad copy generator, and more"
          icon="🛠️"
        />
      </div>

      <div className="rounded-lg border border-gray-200 bg-white p-6">
        <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">
          System Status
        </h2>
        <div className="flex items-center gap-2">
          <span className="h-2.5 w-2.5 rounded-full bg-green-500" />
          <span className="text-sm text-gray-700">
            RM Team AI v0.1.0 — Ready
          </span>
        </div>
      </div>
    </div>
  );
}

function QuickAction({
  href,
  title,
  description,
  icon,
}: {
  href: string;
  title: string;
  description: string;
  icon: string;
}) {
  return (
    <a
      href={href}
      className="block rounded-lg border border-gray-200 bg-white p-6 hover:border-gray-400 hover:shadow-sm transition-all"
    >
      <div className="text-3xl mb-3">{icon}</div>
      <h3 className="font-semibold text-gray-900">{title}</h3>
      <p className="mt-1 text-sm text-gray-500">{description}</p>
    </a>
  );
}
