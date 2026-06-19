import { Routes, Route, Navigate } from "react-router-dom";

// pages
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import RoleDashboard from "./pages/RoleDashboard";
import Tasks from "./pages/Tasks";
import Kanban from "./pages/Kanban";
import Approval from "./pages/Approval";
import DocumentUpload from "./pages/DocumentUpload";
import Notifications from "./pages/Notifications";
import AuditLogs from "./pages/AuditLogs";
import EmployeeDashboard from "./pages/EmployeeDashboard";
import ManagerDashboard from "./pages/ManagerDashboard";
import AdminDashboard from "./pages/AdminDashboard";
import AIInsights from "./pages/AIInsights";
import Subscription from "./pages/Subscription";
import Success from "./pages/Success";
import Cancel from "./pages/Cancel";
import Register from "./pages/Register";
import LeaveRequest from "./pages/LeaveRequest";
import SLARules from "./pages/SLARules";
import SLADashboard from "./pages/SLADashboard";
import ApprovalEscalations from "./pages/ApprovalEscalations";
import ApprovalDelegations from "./pages/ApprovalDelegations";
import NotificationPreferences from "./pages/NotificationPreferences";
import EnhancedAuditLogs from "./pages/EnhancedAuditLogs";
import TenantManagement from "./pages/TenantManagement";
import TenantUsage from "./pages/TenantUsage";
import Workspace from "./pages/Workspace";
import Channel from "./pages/Channel";
import WorkspaceChat from "./pages/WorkspaceChat";
import ChannelChat from "./pages/ChannelChat";
import WorkspaceTasks from "./pages/WorkspaceTasks";
import ChannelTasks from "./pages/ChannelTasks";
import TaskDocuments from "./pages/TaskDocuments";
import ApprovalDocuments from "./pages/ApprovalDocuments";
// components
import AnalyticsChart from "./components/AnalyticsChart";
import NotificationBell from "./components/NotificationBell";

// layouts
import PublicLayout from "./layout/PublicLayout";
import PrivateLayout from "./layout/PrivateLayout";
import RoleGuard from "./routes/RoleGuard";

export default function App() {
  return (
    <Routes>

      <Route path="/" element={<Navigate to="/login" />} />

      <Route element={<PublicLayout />}>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Route>

      <Route element={<PrivateLayout />}>
        <Route path="/dashboard" element={<RoleDashboard />} />
        <Route path="/analytics-dashboard" element={<Dashboard />} />
        <Route path="/tasks" element={<Tasks />} />
        <Route path="/kanban" element={<RoleGuard roles={["admin", "manager"]}><Kanban /></RoleGuard>} />
        <Route path="/approval" element={<RoleGuard roles={["admin", "manager"]}><Approval /></RoleGuard>} />
        <Route path="/leave-request" element={<LeaveRequest />} />
        <Route path="/documents" element={<DocumentUpload />} />
        <Route path="/notifications" element={<Notifications />} />
        <Route path="/audit-logs" element={<AuditLogs />} />
        <Route path="/employee-dashboard" element={<EmployeeDashboard />} />
        <Route path="/manager-dashboard" element={<ManagerDashboard />} />
        <Route path="/admin-dashboard" element={<AdminDashboard />} />
        <Route path="/ai-insights" element={<AIInsights />} />
        <Route path="/subscription" element={<Subscription />} />
        <Route path="/success" element={<Success />} />
        <Route path="/cancel" element={<Cancel />} />
        <Route path="/admin/sla-rules" element={<RoleGuard roles={["admin"]}><SLARules /></RoleGuard>} />
        <Route path="/dashboard/sla" element={<RoleGuard roles={["admin", "manager"]}><SLADashboard /></RoleGuard>} />
        <Route path="/approval-escalations" element={<RoleGuard roles={["admin", "manager"]}><ApprovalEscalations /></RoleGuard>} />
        <Route path="/approval-delegations" element={<RoleGuard roles={["admin", "manager"]}><ApprovalDelegations /></RoleGuard>} />
        <Route path="/settings/notification-preferences" element={<NotificationPreferences />} />
        <Route path="/admin/audit-logs" element={<RoleGuard roles={["admin"]}><EnhancedAuditLogs /></RoleGuard>} />
        <Route path="/admin/tenants" element={<RoleGuard roles={["admin"]}><TenantManagement /></RoleGuard>} />
        <Route path="/dashboard/tenant-usage" element={<RoleGuard roles={["admin", "manager"]}><TenantUsage /></RoleGuard>} />
        <Route path="/workspaces" element={<Workspace />} />
        <Route path="/channels" element={<Channel />} />
        <Route path="/workspace-chat" element={<WorkspaceChat />} />
        <Route path="/channel-chat" element={<ChannelChat />} />
        <Route path="/workspace-tasks" element={<WorkspaceTasks />} />
        <Route path="/channel-tasks" element={<ChannelTasks />} />
        <Route path="/task-documents" element={<TaskDocuments />} />
        <Route path="/approval-documents" element={<ApprovalDocuments />} />
      </Route>

    </Routes>
  );
}
