import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <div className="w-64 h-screen bg-gradient-to-b from-indigo-600 to-purple-600 text-white p-4">
      <h1 className="text-2xl font-bold mb-6">🚀 EC APP</h1>

      <div className="space-y-4">
        <Link to="/dashboard">📊 Dashboard</Link>
        <Link to="/tasks">📝 Tasks</Link>
        <Link to="/kanban">📌 Kanban</Link>
        <Link to="/approval">✅ Approval</Link>
      </div>
    </div>
  );
}