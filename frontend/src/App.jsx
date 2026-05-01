import { Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Tasks from "./pages/Tasks";
import Kanban from "./pages/Kanban";
import Approval from "./pages/Approval";
import Sidebar from "./components/Sidebar";

export default function App() {
  return (
    <div className="flex min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">

      <Sidebar />

      <div className="flex-1 p-6">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/tasks" element={<Tasks />} />
          <Route path="/kanban" element={<Kanban />} />
          <Route path="/approval" element={<Approval />} />
        </Routes>
      </div>

    </div>
  );
}