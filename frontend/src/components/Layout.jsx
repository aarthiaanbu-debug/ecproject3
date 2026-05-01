import { Link, Outlet } from "react-router-dom";

export default function Layout() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">

      {/* NAVBAR */}
      <nav className="flex items-center justify-between px-6 py-4 bg-white/10 backdrop-blur-lg border-b border-white/10">
        <h1 className="text-xl font-bold">🚀 EC APP</h1>

        <div className="flex gap-4 text-sm">
          <Link className="hover:text-purple-300" to="/">📊 Dashboard</Link>
          <Link className="hover:text-purple-300" to="/tasks">📝 Tasks</Link>
          <Link className="hover:text-purple-300" to="/kanban">📌 Kanban</Link>
          <Link className="hover:text-purple-300" to="/approval">✅ Approval</Link>
        </div>
      </nav>

      {/* PAGE CONTENT */}
      <div className="p-6">
        <Outlet />
      </div>
    </div>
  );
}