import { Link, useLocation, useNavigate } from "react-router-dom";
import NotificationBell from "./NotificationBell";

export default function Sidebar() {

  const location = useLocation();
  const navigate = useNavigate();

  // =========================
  // MENU ITEMS (OLD + NEW)
  // =========================
  const menuItems = [
    { path: "/dashboard", label: "📊 Dashboard" },
    { path: "/tasks", label: "📝 Tasks" },
    { path: "/kanban", label: "📌 Kanban" },
    { path: "/approval", label: "✅ Approval" },
    { path: "/documents", label: "📂 Documents" },

    // ✅ NEW SUBSCRIPTION ADDED
    { path: "/subscription", label: "💳 Subscription" },
  ];

  // =========================
  // LOGOUT
  // =========================
  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div className="w-64 min-h-screen bg-slate-900 text-white p-5 shadow-2xl flex flex-col">

      {/* ================= HEADER ================= */}
      <div className="flex items-center justify-between mb-10">

        <div>
          <h1 className="text-3xl font-extrabold tracking-wide">
            🚀 EC APP
          </h1>
          <p className="text-gray-400 text-sm mt-1">
            Enterprise Workflow
          </p>
        </div>

        <NotificationBell />

      </div>

      {/* ================= MENU ================= */}
      <div className="space-y-4 flex-1">

        {menuItems.map((item) => {

          const isActive = location.pathname === item.path;

          return (
            <Link
              key={item.path}
              to={item.path}
              className={`
                block p-4 rounded-2xl transition-all duration-300 font-semibold shadow-md border border-white/10

                ${isActive
                  ? "bg-blue-600 text-white scale-[1.02] shadow-blue-500/30"
                  : "bg-white/10 hover:bg-white/20 text-gray-100"
                }
              `}
            >
              <div className="flex items-center justify-between">
                <span>{item.label}</span>
                {isActive && <span className="text-xs">●</span>}
              </div>
            </Link>
          );
        })}

      </div>

      {/* ================= STATUS BOX ================= */}
      <div className="pt-6 border-t border-white/10">

        <div className="bg-white/5 rounded-2xl p-4">

          <h2 className="font-bold text-lg mb-1">
            💡 Status
          </h2>

          <p className="text-sm text-gray-400">
            System running normally
          </p>

        </div>

        {/* ================= LOGOUT ================= */}
        <button
          onClick={handleLogout}
          className="w-full mt-4 bg-red-600 hover:bg-red-700 transition p-3 rounded-xl font-semibold"
        >
          🚪 Logout
        </button>

      </div>

    </div>
  );
}