import EmployeeDashboard from "./EmployeeDashboard";
import ManagerDashboard from "./ManagerDashboard";
import AdminDashboard from "./AdminDashboard";

export default function RoleDashboard() {
  const role = localStorage.getItem("role");

  if (role === "admin") return <AdminDashboard />;
  if (role === "manager") return <ManagerDashboard />;

  return <EmployeeDashboard />;
}
export default function EmployeeDashboard() {
  return (
    <div className="text-white">
      <h1>Employee Panel</h1>
      <p>My Tasks + My Requests</p>
    </div>
  );
}
export default function ManagerDashboard() {
  return (
    <div className="text-white">
      <h1>Manager Panel</h1>
      <p>Team tracking + Approvals</p>
    </div>
  );
}
export default function AdminDashboard() {
  return (
    <div className="text-white">
      <h1>Admin Panel</h1>
      <p>System Analytics + Monitoring</p>
    </div>
  );
}