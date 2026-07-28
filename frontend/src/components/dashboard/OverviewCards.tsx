import { useEffect, useState } from "react";

import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import { getDashboardData } from "@/services/api";

import {
  IconShieldCheck,
  IconActivityHeartbeat,
  IconDeviceDesktopAnalytics,
  IconBrain,
} from "@tabler/icons-react";

type DashboardData = {
  active_threats: number;
  packets_per_second: number;
  connected_hosts: number;
  ai_confidence: number;
};

export default function OverviewCards() {
  const [data, setData] = useState<DashboardData>({
    active_threats: 0,
    packets_per_second: 0,
    connected_hosts: 0,
    ai_confidence: 0,
  });

  async function loadDashboard() {
    try {
      const response = await getDashboardData();

      console.log("📊 Updated dashboard data:", response);

      setData(response);
    } catch (error) {
      console.error(
        "Failed to load dashboard:",
        error
      );
    }
  }

  useEffect(() => {
    // Load data when dashboard first opens
    loadDashboard();

    // Reload whenever a live alert arrives
    const handleDashboardUpdate = () => {
      console.log("🔄 Refreshing overview cards...");
      loadDashboard();
    };

    window.addEventListener(
      "dashboard-update",
      handleDashboardUpdate
    );

    return () => {
      window.removeEventListener(
        "dashboard-update",
        handleDashboardUpdate
      );
    };
  }, []);

  const cards = [
    {
      title: "Active Threats",
      value: data.active_threats,
      change: "Live",
      color: "red" as const,
      icon: IconShieldCheck,
    },
    {
      title: "Packets / sec",
      value: data.packets_per_second,
      change: "Live",
      color: "blue" as const,
      icon: IconActivityHeartbeat,
    },
    {
      title: "Connected Hosts",
      value: data.connected_hosts,
      change: "Online",
      color: "yellow" as const,
      icon: IconDeviceDesktopAnalytics,
    },
    {
      title: "AI Confidence",
      value: `${data.ai_confidence}%`,
      change: "Stable",
      color: "green" as const,
      icon: IconBrain,
    },
  ];

  return (
    <div className="grid grid-cols-4 gap-6">
      {cards.map((card) => {
        const Icon = card.icon;

        return (
          <Card key={card.title}>
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-zinc-500">
                  {card.title}
                </p>

                <h2 className="mt-3 text-3xl font-bold">
                  {card.value}
                </h2>

                <div className="mt-4">
                  <Badge
                    text={card.change}
                    color={card.color}
                  />
                </div>
              </div>

              <div className="rounded-xl bg-zinc-900 p-3">
                <Icon
                  size={24}
                  className="text-zinc-300"
                />
              </div>
            </div>
          </Card>
        );
      })}
    </div>
  );
}