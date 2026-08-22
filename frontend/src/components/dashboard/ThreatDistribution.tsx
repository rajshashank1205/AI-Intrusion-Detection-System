import { useEffect, useState } from "react";
import {
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
} from "recharts";

type Threat = {
  severity: string;
  total: number;
};

const colors: Record<string, string> = {
  CRITICAL: "#ef4444",
  HIGH: "#f59e0b",
  MEDIUM: "#3b82f6",
  LOW: "#22c55e",
};

export default function ThreatDistribution() {
  const [data, setData] = useState<Threat[]>([]);

  async function loadThreatDistribution() {
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/threat-distribution`
      );

      const result = await response.json();

      setData(result);
    } catch (error) {
      console.error("Failed to load threat distribution:", error);
    }
  }

  useEffect(() => {
    loadThreatDistribution();

    const interval = setInterval(loadThreatDistribution, 5000);

    return () => clearInterval(interval);
  }, []);

  const totalThreats = data.reduce(
    (sum, item) => sum + item.total,
    0
  );

  return (
    <div className="h-full rounded-2xl border border-zinc-800 bg-zinc-900 p-6">

      <div className="mb-6">
        <h2 className="text-lg font-semibold">
          Threat Distribution
        </h2>

        <p className="text-sm text-zinc-500">
          Severity of detected alerts
        </p>
      </div>

      <div className="flex h-[220px] items-center">

        <div className="h-full w-1/2">

          <ResponsiveContainer width="100%" height="100%">

            <PieChart>

              <Pie
                data={data}
                dataKey="total"
                nameKey="severity"
                innerRadius={55}
                outerRadius={82}
                paddingAngle={4}
              >
                {data.map((entry) => (
                  <Cell
                    key={entry.severity}
                    fill={
                      colors[entry.severity.toUpperCase()] ??
                      "#71717a"
                    }
                  />
                ))}
              </Pie>

            </PieChart>

          </ResponsiveContainer>

        </div>

        <div className="flex-1 space-y-4">

          {data.map((item) => {

            const percentage =
              totalThreats === 0
                ? 0
                : Math.round(
                    (item.total / totalThreats) * 100
                  );

            return (

              <div
                key={item.severity}
                className="flex items-center justify-between"
              >

                <div className="flex items-center gap-3">

                  <div
                    className="h-3 w-3 rounded-full"
                    style={{
                      backgroundColor:
                        colors[item.severity.toUpperCase()] ??
                        "#71717a",
                    }}
                  />

                  <span className="text-sm text-zinc-300">
                    {item.severity}
                  </span>

                </div>

                <span className="font-medium">
                  {percentage}%
                </span>

              </div>

            );
          })}

        </div>

      </div>

    </div>
  );
}