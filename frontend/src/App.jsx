import { Routes, Route, Navigate } from "react-router-dom";

// pages
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
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
import SLARules from "./pages/SLARules";
import SLADashboard from "./pages/SLADashboard";
import ApprovalEscalations from "./pages/ApprovalEscalations";
import ApprovalDelegations from "./pages/ApprovalDelegations";
import NotificationPreferences from "./pages/NotificationPreferences";
import EnhancedAuditLogs from "./pages/EnhancedAuditLogs";

// components
import AnalyticsChart from "./components/AnalyticsChart";
import NotificationBell from "./components/NotificationBell";

// layouts
import PublicLayout from "./layout/PublicLayout";
import PrivateLayout from "./layout/PrivateLayout";

export default function App() {
  return (
    <Routes>

      <Route path="/" element={<Navigate to="/login" />} />

      <Route element={<PublicLayout />}>
        <Route path="/login" element={<Login />} />
      </Route>

      <Route element={<PrivateLayout />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/tasks" element={<Tasks />} />
        <Route path="/kanban" element={<Kanban />} />
        <Route path="/approval" element={<Approval />} />
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
        <Route path="/admin/sla-rules" element={<SLARules />} />
        <Route path="/dashboard/sla" element={<SLADashboard />} />
        <Route path="/approval-escalations" element={<ApprovalEscalations />} />
        <Route path="/approval-delegations" element={<ApprovalDelegations />} />
        <Route path="/settings/notification-preferences" element={<NotificationPreferences />} />
        <Route path="/admin/audit-logs" element={<EnhancedAuditLogs />} />
      </Route>

    </Routes>
  );
}
