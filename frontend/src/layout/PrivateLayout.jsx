import { Outlet } from "react-router-dom";
import Sidebar from "../components/Sidebar";

export default function PrivateLayout() {
  return (
    <div className="flex min-h-screen bg-slate-900 text-white">

      {/* SIDEBAR */}
      <Sidebar />

      {/* MAIN CONTENT */}
      <div className="flex-1 p-6 overflow-auto">
        <Outlet />
      </div>

    </div>
  );
}