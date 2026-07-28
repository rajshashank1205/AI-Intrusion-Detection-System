import { Routes, Route } from "react-router-dom";

import Sidebar from "@/components/layout/Sidebar";
import TopNavbar from "@/components/layout/Topbar";
import DashboardLayout from "@/components/dashboard/DashboardLayout";

import LiveTraffic from "@/pages/live-traffic/LiveTraffic";
import ThreatAnalysis from "@/pages/threat-analysis/ThreatAnalysis";
import Incidents from "@/pages/incidents/Incidents";
import Settings from "@/pages/settings/Settings";


export default function App() {

  return (

    <div className="flex h-screen bg-zinc-950 text-white">

      <Sidebar />

      <div className="flex flex-1 flex-col overflow-hidden">

        <TopNavbar />

        <main className="flex-1 overflow-auto p-8">

          <Routes>

            {/* Dashboard */}

            <Route
              path="/"
              element={
                <DashboardLayout />
              }
            />

            {/* Live Traffic */}

            <Route
              path="/live-traffic"
              element={
                <LiveTraffic />
              }
            />

            {/* Threat Analysis */}

            <Route
              path="/threat-analysis"
              element={
                <ThreatAnalysis />
              }
            />

            {/* Incidents */}

            <Route
              path="/incidents"
              element={
                <Incidents />
              }
            />

            {/* Settings */}

            <Route
              path="/settings"
              element={
                <Settings />
              }
            />

          </Routes>

        </main>

      </div>

    </div>

  );

}