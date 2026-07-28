import {
  IconActivityHeartbeat,
  IconAlertTriangle,
  IconDashboard,
  IconSettings,
  IconShieldLock,
} from "@tabler/icons-react";

import { NavLink } from "react-router-dom";


const menu = [
  {
    title: "Dashboard",
    icon: IconDashboard,
    path: "/",
  },
  {
    title: "Live Traffic",
    icon: IconActivityHeartbeat,
    path: "/live-traffic",
  },
  {
    title: "Threat Analysis",
    icon: IconShieldLock,
    path: "/threat-analysis",
  },
  {
    title: "Incidents",
    icon: IconAlertTriangle,
    path: "/incidents",
  },
  {
    title: "Settings",
    icon: IconSettings,
    path: "/settings",
  },
];


export default function Sidebar() {

  return (

    <aside className="flex w-72 flex-col border-r border-zinc-800 bg-zinc-950">

      {/* Logo */}

      <div className="border-b border-zinc-800 px-8 py-8">

        <h1 className="text-2xl font-bold tracking-wide text-white">
          AI IDS
        </h1>

        <p className="mt-2 text-sm text-zinc-500">
          Security Operations
        </p>

      </div>


      {/* Menu */}

      <nav className="flex-1 px-4 py-6">

        {menu.map((item) => {

          const Icon = item.icon;

          return (

            <NavLink
              key={item.title}
              to={item.path}
              end={item.path === "/"}
              className={({ isActive }) => `
                mb-1
                flex
                w-full
                items-center
                gap-4
                rounded-lg
                px-4
                py-3
                text-[15px]
                font-medium
                transition-all
                duration-200
                ${
                  isActive
                    ? "bg-blue-600 text-white"
                    : "text-zinc-400 hover:bg-zinc-900 hover:text-white"
                }
              `}
            >

              <Icon
                size={22}
                stroke={1.8}
              />

              <span>
                {item.title}
              </span>

            </NavLink>

          );

        })}

      </nav>


      {/* Footer */}

      <div className="border-t border-zinc-800 p-6">

        <div className="flex items-center gap-3">

          <div className="
            flex
            h-11
            w-11
            items-center
            justify-center
            rounded-full
            bg-blue-600
            font-bold
            text-white
          ">
            S
          </div>

          <div>

            <p className="font-medium text-white">
              Shashank
            </p>

            <p className="text-sm text-zinc-500">
              Administrator
            </p>

          </div>

        </div>

      </div>

    </aside>

  );
}