import { Link, useLocation, useNavigate } from "react-router-dom";
import NotificationBell from "./NotificationBell";

export default function Sidebar() {
  const location = useLocation();
  const navigate = useNavigate();

  const menuItems = [
    { path: "/dashboard", label: "Dashboard" },
    { path: "/analytics-dashboard", label: "Analytics Dashboard" },
    { path: "/tasks", label: "Tasks" },
    { path: "/kanban", label: "Kanban" },
    { path: "/approval", label: "Approval" },
    { path: "/leave-request", label: "Leave Requests" },
    { path: "/documents", label: "Documents" },
    { path: "/notifications", label: "Notifications" },
    { path: "/dashboard/sla", label: "SLA Dashboard" },
    { path: "/admin/sla-rules", label: "SLA Rules" },
    { path: "/approval-escalations", label: "Approval Escalations" },
    { path: "/approval-delegations", label: "Approval Delegations" },
    { path: "/settings/notification-preferences", label: "Notification Preferences" },
    { path: "/admin/audit-logs", label: "Audit Logs" },
    { path: "/admin/tenants", label: "Tenant Management" },
    { path: "/dashboard/tenant-usage", label: "Tenant Usage" },
    { path: "/subscription", label: "Subscription" },
    { path: "/workspaces", label: "Workspaces" },
    { path: "/channels", label: "Channels" },
    { path: "/workspace-chat", label: "Workspace Chat" },
{ path: "/channel-chat", label: "Channel Chat" },

{ path: "/workspace-tasks", label: "Workspace Tasks" },
{ path: "/channel-tasks", label: "Channel Tasks" },

{ path: "/task-documents", label: "Task Documents" },
{ path: "/approval-documents", label: "Approval Documents" },
{ path: "/teams", label: "Teams" },
{ path: "/projects", label: "Projects" },
{ path: "/project-teams", label: "Project Teams" },
{ path: "/project-channels", label: "Project Channels" },
{ path: "/project-tasks", label: "Project Tasks" },
{ path: "/project-documents", label: "Project Documents" },
{ path: "/meeting-scheduler", label: "Meeting Scheduler" },
{ path: "/meeting-notes", label: "Meeting Notes" },
{ path: "/ai-meeting-summary", label: "AI Meeting Summary" },
{ path: "/project-calendar", label: "Project Calendar" },
{ path: "/team-workload-dashboard", label: "Team Workload" },
{ path: "/workflow-builder", label: "Workflow Builder" },
{ path: "/notification-rules", label: "Notification Rules" },
{ path: "/global-search", label: "Global Search" },
{ path: "/saved-searches", label: "Saved Searches" },
{ path: "/phase10d/analytics", label: "Analytics Dashboard" },
{ path: "/analytics/projects", label: "Project Analytics" },
{ path: "/analytics/teams", label: "Team Analytics" },
{ path: "/analytics/tasks", label: "Task Analytics" },
{ path: "/analytics/approvals", label: "Approval Analytics" },
{ path: "/analytics/documents", label: "Document Analytics" },
{ path: "/knowledge-base", label: "Knowledge Base" },
{ path: "/article-editor", label: "Article Editor" },
{ path: "/custom-forms", label: "Custom Forms" },
{ path: "/reports", label: "Reports" },
  ];

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
    localStorage.removeItem("user_id");
    localStorage.removeItem("tenant_id");
    localStorage.removeItem("role");
    navigate("/login");
  };

  return (
    <div className="w-64 min-h-screen bg-slate-900 text-white p-5 shadow-2xl flex flex-col">
      <div className="flex items-center justify-between mb-8">
        <button
          type="button"
          onClick={() => navigate("/dashboard")}
          className="text-left"
          title="Go to dashboard"
        >
          <h1 className="text-3xl font-extrabold tracking-wide">EC APP</h1>
          <p className="text-gray-400 text-sm mt-1">Enterprise Workflow</p>
        </button>
        <NotificationBell />
      </div>

      <div className="space-y-3 flex-1 overflow-y-auto pr-1">
        {menuItems.map((item) => {
          const isActive = location.pathname === item.path;

          return (
            <Link
              key={item.path}
              to={item.path}
              className={`block rounded-xl border border-white/10 p-3 font-semibold transition ${
                isActive
                  ? "bg-blue-600 text-white shadow-blue-500/30"
                  : "bg-white/10 text-gray-100 hover:bg-white/20"
              }`}
            >
              {item.label}
            </Link>
          );
        })}
      </div>

      <div className="pt-6 border-t border-white/10">
        <div className="bg-white/5 rounded-2xl p-4">
          <h2 className="font-bold text-lg mb-1">Status</h2>
          <p className="text-sm text-gray-400">System running normally</p>
        </div>

        <button
          onClick={handleLogout}
          className="w-full mt-4 bg-red-600 hover:bg-red-700 transition p-3 rounded-xl font-semibold"
        >
          Logout
        </button>
      </div>
    </div>
  );
}
