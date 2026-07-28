import OverviewCards from "./OverviewCards";
import ThreatCharts from "./ThreatChart";
import RecentAlerts from "./RecentAlerts";
import ThreatDistribution from "./ThreatDistribution";
import TopHosts from "./TopHosts";

export default function DashboardLayout() {
  return (
    <div className="space-y-8">

      {/* Header */}

      <div>
        <h1 className="text-4xl font-bold tracking-tight">
          Dashboard
        </h1>

        <p className="mt-2 text-zinc-500">
          Real-time overview of your network security.
        </p>
      </div>

      {/* Overview Cards */}

      <OverviewCards />

      {/* Top Row */}

      <div className="grid grid-cols-3 gap-6">

        <div className="col-span-2">
          <ThreatCharts />
        </div>

        <RecentAlerts />

      </div>

      {/* Bottom Row */}

      <div className="grid grid-cols-2 gap-6">

        <ThreatDistribution />

        <TopHosts />

      </div>

    </div>
  );
}