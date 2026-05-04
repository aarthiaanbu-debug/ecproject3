// Sidebar.jsx

import { Link, useLocation } from "react-router-dom";
import NotificationBell from "./NotificationBell";

export default function Sidebar() {

  const location = useLocation();

  const menuItems = [
    {
      path: "/dashboard",
      label: "📊 Dashboard",
    },
    {
      path: "/tasks",
      label: "📝 Tasks",
    },
    {
      path: "/kanban",
      label: "📌 Kanban",
    },
    {
      path: "/approval",
      label: "✅ Approval",
    },
    {
      path: "/documents",
      label: "📂 Documents",
    },
  ];

  return (

    <div
      className="
        w-64
        min-h-screen
        bg-slate-900
        text-white
        p-5
        shadow-2xl
        flex
        flex-col
      "
    >

      {/* ========================= */}
      {/* HEADER */}
      {/* ========================= */}

      <div className="flex items-center justify-between mb-10">

        <div>

          <h1 className="text-3xl font-extrabold tracking-wide">
            🚀 EC APP
          </h1>

          <p className="text-gray-400 text-sm mt-1">
            Enterprise Workflow
          </p>

        </div>

        {/* NOTIFICATION BELL */}
        <NotificationBell />

      </div>

      {/* ========================= */}
      {/* MENU */}
      {/* ========================= */}

      <div className="space-y-4 flex-1">

        {menuItems.map((item) => (

          <Link
            key={item.path}
            to={item.path}
            className={`
              block
              p-4
              rounded-2xl
              transition-all
              duration-300
              font-semibold
              shadow-md
              border
              border-white/10

              ${
                location.pathname === item.path
                  ? "bg-blue-600 text-white scale-[1.02] shadow-blue-500/30"
                  : "bg-white/10 hover:bg-white/20 text-gray-100"
              }
            `}
          >

            <div className="flex items-center justify-between">

              <span>
                {item.label}
              </span>

              {location.pathname === item.path && (
                <span className="text-xs">
                  ●
                </span>
              )}

            </div>

          </Link>

        ))}

      </div>

      {/* ========================= */}
      {/* FOOTER */}
      {/* ========================= */}

      <div className="pt-6 border-t border-white/10">

        <div className="bg-white/5 rounded-2xl p-4">

          <h2 className="font-bold text-lg mb-1">
            💡 Status
          </h2>

          <p className="text-sm text-gray-400">
            System running normally
          </p>

        </div>

      </div>

    </div>
  );
}