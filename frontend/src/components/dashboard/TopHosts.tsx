import { useEffect, useState } from "react";

type Host = {
  source_ip: string;
  total: number;
};

export default function TopHosts() {
  const [hosts, setHosts] = useState<Host[]>([]);

  async function loadHosts() {
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/top-hosts`
      );

      const data = await response.json();

      setHosts(data);
    } catch (error) {
      console.error("Failed to load hosts:", error);
    }
  }

  useEffect(() => {
    loadHosts();

    const interval = setInterval(loadHosts, 5000);

    return () => clearInterval(interval);
  }, []);

  const maxAlerts =
    hosts.length > 0 ? hosts[0].total : 1;

  return (
    <div className="h-full rounded-2xl border border-zinc-800 bg-zinc-900 p-6">

      <div className="mb-6">
        <h2 className="text-lg font-semibold">
          Top Active Hosts
        </h2>

        <p className="text-sm text-zinc-500">
          Hosts generating the most alerts
        </p>
      </div>

      <div className="space-y-5">

        {hosts.map((host) => (

          <div key={host.source_ip}>

            <div className="mb-2 flex justify-between text-sm">

              <span>{host.source_ip}</span>

              <span>{host.total} alerts</span>

            </div>

            <div className="h-2 rounded-full bg-zinc-800">

              <div
                className="h-2 rounded-full bg-blue-500 transition-all duration-500"
                style={{
                  width: `${(host.total / maxAlerts) * 100}%`,
                }}
              />

            </div>

          </div>

        ))}

      </div>

    </div>
  );
}