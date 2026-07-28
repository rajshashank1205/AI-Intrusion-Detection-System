import { useLiveData } from "@/context/LiveDataContext";

export default function RecentAlerts() {
  const { alerts } = useLiveData();

  return (
    <div className="flex h-full flex-col rounded-2xl border border-zinc-800 bg-zinc-900 p-6">

      <div className="mb-5">
        <h2 className="text-lg font-semibold">
          Recent Alerts
        </h2>

        <p className="text-sm text-zinc-500">
          Live alerts from the IDS
        </p>
      </div>

      <div className="space-y-4">

        {alerts.length === 0 ? (
          <div className="rounded-xl border border-zinc-800 bg-zinc-950 p-4 text-center text-zinc-500">
            No live alerts yet...
          </div>
        ) : (
          alerts.map((alert, index) => {

            let color = "bg-blue-500";

            if (alert.severity === "CRITICAL")
              color = "bg-red-500";
            else if (alert.severity === "HIGH")
              color = "bg-orange-500";
            else if (alert.severity === "MEDIUM")
              color = "bg-yellow-500";
            else if (alert.severity === "LOW")
              color = "bg-green-500";

            return (
              <div
                key={index}
                className="rounded-xl border border-zinc-800 bg-zinc-950 p-4 transition-all duration-200 hover:border-blue-500 hover:bg-zinc-900"
              >
                <div className="flex items-center justify-between">

                  <div className="flex items-center gap-3">

                    <div
                      className={`h-3 w-3 rounded-full ${color}`}
                    />

                    <div>
                      <h3 className="font-medium">
                        {alert.alert_type}
                      </h3>

                      <p className="text-xs text-zinc-500">
                        {alert.source_ip}
                      </p>
                    </div>

                  </div>

                  <span className="text-xs text-zinc-500">
                    {alert.severity}
                  </span>

                </div>
              </div>
            );
          })
        )}

      </div>

    </div>
  );
}