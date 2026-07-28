import { useEffect, useState } from "react";

import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { getDashboardData } from "@/services/api";


type TrafficPoint = {
  time: string;
  packets: number;
};


export default function ThreatCharts() {

  const [data, setData] = useState<TrafficPoint[]>([]);


  useEffect(() => {

    let isMounted = true;

    async function updateTraffic() {

      try {

        const dashboardData = await getDashboardData();

        if (!isMounted) return;

        const newPoint: TrafficPoint = {

          time: new Date().toLocaleTimeString(
            [],
            {
              hour: "2-digit",
              minute: "2-digit",
              second: "2-digit",
            }
          ),

          packets: dashboardData.packets_per_second,
        };


        setData((previousData) => {

          const updatedData = [
            ...previousData,
            newPoint,
          ];

          // Keep only the latest 30 readings
          return updatedData.slice(-30);

        });

      } catch (error) {

        console.error(
          "Failed to update live traffic graph:",
          error
        );

      }

    }


    // Get first reading immediately
    updateTraffic();


    // Get a new reading every second
    const interval = setInterval(
      updateTraffic,
      1000
    );


    return () => {

      isMounted = false;

      clearInterval(interval);

    };

  }, []);


  return (

    <div className="h-full rounded-2xl border border-zinc-800 bg-zinc-900 p-6">

      <div className="mb-6 flex items-center justify-between">

        <div>

          <h2 className="text-lg font-semibold">
            Live Network Traffic
          </h2>

          <p className="text-sm text-zinc-500">
            Packets per second
          </p>

        </div>


        <div className="rounded-full bg-green-500/20 px-3 py-1 text-xs text-green-400">
          LIVE
        </div>

      </div>


      <ResponsiveContainer
        width="100%"
        height={270}
      >

        <AreaChart data={data}>

          <defs>

            <linearGradient
              id="traffic"
              x1="0"
              y1="0"
              x2="0"
              y2="1"
            >

              <stop
                offset="0%"
                stopColor="#2563eb"
                stopOpacity={0.8}
              />

              <stop
                offset="100%"
                stopColor="#2563eb"
                stopOpacity={0}
              />

            </linearGradient>

          </defs>


          <CartesianGrid
            stroke="#27272a"
            strokeDasharray="3 3"
          />


          <XAxis
            dataKey="time"
            stroke="#71717a"
            minTickGap={30}
          />


          <YAxis
            stroke="#71717a"
            allowDecimals={false}
          />


          <Tooltip />


          <Area
            type="monotone"
            dataKey="packets"
            stroke="#3b82f6"
            strokeWidth={3}
            fill="url(#traffic)"
            isAnimationActive={false}
          />

        </AreaChart>

      </ResponsiveContainer>

    </div>

  );
}