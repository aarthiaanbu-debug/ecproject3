import { useEffect, useMemo, useState } from "react";
import DataTable from "../components/ui/DataTable";
import ErrorMessage from "../components/ui/ErrorMessage";
import PageHeader from "../components/ui/PageHeader";
import StatusBadge from "../components/ui/StatusBadge";
import {
  assignUserToTenant,
  createTenant,
  getTenants,
  getUsers,
  updateTenant,
} from "../services/api";

const emptyTenant = {
  name: "",
  domain: "",
  plan: "basic",
};

export default function TenantManagement() {
  const [tenants, setTenants] = useState([]);
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState(emptyTenant);
  const [editingId, setEditingId] = useState(null);
  const [assignment, setAssignment] = useState({
    user_id: "",
    organization_id: "",
  });
  const [filter, setFilter] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const load = async () => {
    try {
      const [tenantRes, userRes] = await Promise.all([getTenants(), getUsers()]);
      setTenants(tenantRes.data || []);
      setUsers(userRes.data || []);
    } catch (err) {
      console.log(err);
      setError("Unable to load tenant data");
    }
  };

  useEffect(() => {
    load();
  }, []);

  const filteredTenants = useMemo(() => {
    const value = filter.toLowerCase().trim();
    if (!value) return tenants;

    return tenants.filter(
      (tenant) =>
        tenant.name?.toLowerCase().includes(value) ||
        tenant.domain?.toLowerCase().includes(value) ||
        tenant.plan?.toLowerCase().includes(value)
    );
  }, [tenants, filter]);

  const submitTenant = async (event) => {
    event.preventDefault();

    if (!form.name.trim()) {
      setError("Tenant name is required");
      return;
    }

    try {
      if (editingId) {
        await updateTenant(editingId, form);
        setSuccess("Tenant updated");
      } else {
        await createTenant(form);
        setSuccess("Tenant created");
      }

      setForm(emptyTenant);
      setEditingId(null);
      setError("");
      load();
    } catch (err) {
      console.log(err);
      setError(err.response?.data?.detail || "Unable to save tenant");
    }
  };

  const submitAssignment = async (event) => {
    event.preventDefault();

    if (!assignment.user_id || !assignment.organization_id) {
      setError("Select user and tenant");
      return;
    }

    try {
      await assignUserToTenant({
        user_id: Number(assignment.user_id),
        organization_id: Number(assignment.organization_id),
      });
      setAssignment({ user_id: "", organization_id: "" });
      setSuccess("User assigned to tenant");
      setError("");
      load();
    } catch (err) {
      console.log(err);
      setError(err.response?.data?.detail || "Unable to assign user");
    }
  };

  const editTenant = (tenant) => {
    setEditingId(tenant.id);
    setForm({
      name: tenant.name || "",
      domain: tenant.domain || "",
      plan: tenant.plan || "basic",
      is_active: tenant.is_active ?? 1,
    });
  };

  const columns = [
    { key: "id", label: "Tenant ID" },
    { key: "name", label: "Name" },
    { key: "domain", label: "Domain" },
    { key: "plan", label: "Plan" },
    {
      key: "is_active",
      label: "Status",
      render: (tenant) => (
        <StatusBadge value={tenant.is_active ? "active" : "disabled"} />
      ),
    },
    {
      key: "actions",
      label: "Actions",
      render: (tenant) => (
        <button onClick={() => editTenant(tenant)} className="text-blue-600">
          Edit
        </button>
      ),
    },
  ];

  return (
    <div className="p-6">
      <PageHeader
        title="Tenant Management"
        subtitle="Create tenants and assign users for collaboration tracking"
      />

      <ErrorMessage message={error} />
      {success && (
        <div className="mb-4 rounded-lg bg-green-500/20 p-3 text-green-200">
          {success}
        </div>
      )}

      <div className="mb-6 grid gap-4 lg:grid-cols-2">
        <form onSubmit={submitTenant} className="rounded-lg bg-white/10 p-4">
          <h2 className="mb-3 text-lg font-semibold text-white">
            {editingId ? "Edit Tenant" : "Create Tenant"}
          </h2>
          <div className="grid gap-3 md:grid-cols-2">
            <input
              value={form.name}
              onChange={(event) => setForm({ ...form, name: event.target.value })}
              className="rounded bg-slate-900 p-2 text-white"
              placeholder="Tenant name"
            />
            <input
              value={form.domain}
              onChange={(event) =>
                setForm({ ...form, domain: event.target.value })
              }
              className="rounded bg-slate-900 p-2 text-white"
              placeholder="Domain"
            />
            <select
              value={form.plan}
              onChange={(event) => setForm({ ...form, plan: event.target.value })}
              className="rounded bg-slate-900 p-2 text-white"
            >
              <option value="basic">Basic</option>
              <option value="pro">Pro</option>
              <option value="enterprise">Enterprise</option>
            </select>
            <button className="rounded bg-blue-600 px-4 py-2 text-white">
              {editingId ? "Update Tenant" : "Create Tenant"}
            </button>
          </div>
        </form>

        <form onSubmit={submitAssignment} className="rounded-lg bg-white/10 p-4">
          <h2 className="mb-3 text-lg font-semibold text-white">
            Assign User to Tenant
          </h2>
          <div className="grid gap-3 md:grid-cols-3">
            <select
              value={assignment.user_id}
              onChange={(event) =>
                setAssignment({ ...assignment, user_id: event.target.value })
              }
              className="rounded bg-slate-900 p-2 text-white"
            >
              <option value="">Select user</option>
              {users.map((user) => (
                <option key={user.id} value={user.id}>
                  {user.name || user.email}
                </option>
              ))}
            </select>
            <select
              value={assignment.organization_id}
              onChange={(event) =>
                setAssignment({
                  ...assignment,
                  organization_id: event.target.value,
                })
              }
              className="rounded bg-slate-900 p-2 text-white"
            >
              <option value="">Select tenant</option>
              {tenants.map((tenant) => (
                <option key={tenant.id} value={tenant.id}>
                  {tenant.name}
                </option>
              ))}
            </select>
            <button className="rounded bg-cyan-600 px-4 py-2 text-white">
              Assign
            </button>
          </div>
        </form>
      </div>

      <div className="mb-4">
        <input
          value={filter}
          onChange={(event) => setFilter(event.target.value)}
          className="w-full rounded bg-slate-900 p-2 text-white md:w-80"
          placeholder="Search tenant, domain, or plan"
        />
      </div>

      <DataTable columns={columns} rows={filteredTenants} />
    </div>
  );
}
