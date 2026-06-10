import AdminDashboard from "./AdminDashboard";
import EmployeeDashboard from "./EmployeeDashboard";
import ManagerDashboard from "./ManagerDashboard";

export default function RoleDashboard() {
  const role = localStorage.getItem("role") || "employee";

  if (role === "admin") return <AdminDashboard />;
  if (role === "manager") return <ManagerDashboard />;

  return <EmployeeDashboard />;
}
