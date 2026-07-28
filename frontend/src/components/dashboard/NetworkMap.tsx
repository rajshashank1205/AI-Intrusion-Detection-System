import OverviewCards from "./OverviewCards";
import ThreatCharts from "./ThreatChart";
import RecentAlerts from "./RecentAlerts";
import ThreatDistribution from "./ThreatDistribution";
import NetworkMap from "./NetworkMap";

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

      {/* Main Dashboard */}
      <div className="grid grid-cols-3 gap-6">
        {/* Live Traffic Chart */}
        <div className="col-span-2 h-[380px]">
          <ThreatCharts />
        </div>

        {/* Recent Alerts */}
        <div className="h-[380px]">
          <RecentAlerts />
        </div>
      </div>

      {/* Bottom Widgets */}
      <div className="grid grid-cols-2 gap-6">
        {/* Threat Distribution */}
        <div className="h-[320px]">
          <ThreatDistribution />
        </div>

        {/* Network Activity */}
        <div className="h-[320px]">
          <NetworkMap />
        </div>
      </div>
    </div>
  );
}