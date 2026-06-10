import { useEffect, useMemo, useState } from "react";
import DataTable from "../components/ui/DataTable";
import ErrorMessage from "../components/ui/ErrorMessage";
import PageHeader from "../components/ui/PageHeader";
import { getAllTenantUsage, getTenants } from "../services/api";

export default function TenantUsage() {
  const [usage, setUsage] = useState([]);
  const [tenants, setTenants] = useState([]);
  const [tenantFilter, setTenantFilter] = useState("");
  const [error, setError] = useState("");

  const load = async () => {
    try {
      const [usageRes, tenantRes] = await Promise.all([
        getAllTenantUsage(),
        getTenants(),
      ]);
      setUsage(usageRes.data || []);
      setTenants(tenantRes.data || []);
      setError("");
    } catch (err) {
      console.log(err);
      setError("Unable to load tenant usage");
    }
  };

  useEffect(() => {
    load();
  }, []);

  const tenantNameById = useMemo(
    () =>
      tenants.reduce((map, tenant) => {
        map[tenant.id] = tenant.name;
        return map;
      }, {}),
    [tenants]
  );

  const filteredUsage = useMemo(() => {
    if (!tenantFilter) return usage;
    return usage.filter((row) => String(row.organization_id) === tenantFilter);
  }, [usage, tenantFilter]);

  const totals = filteredUsage.reduce(
    (summary, row) => ({
      users: summary.users + (row.users_count || 0),
      tasks: summary.tasks + (row.tasks_count || 0),
      approvals: summary.approvals + (row.approvals_count || 0),
      documents: summary.documents + (row.documents_count || 0),
    }),
    { users: 0, tasks: 0, approvals: 0, documents: 0 }
  );

  const columns = [
    {
      key: "organization_id",
      label: "Tenant",
      render: (row) =>
        tenantNameById[row.organization_id] || `Tenant #${row.organization_id}`,
    },
    { key: "users_count", label: "Users" },
    { key: "tasks_count", label: "Tasks" },
    { key: "approvals_count", label: "Approvals" },
    { key: "documents_count", label: "Documents" },
    { key: "comments_count", label: "Comments" },
    { key: "notifications_count", label: "Notifications" },
    { key: "last_activity_at", label: "Last Activity" },
  ];

  return (
    <div className="p-6">
      <PageHeader
        title="Tenant Collaboration Usage"
        subtitle="Track collaboration activity by tenant"
      />
      <ErrorMessage message={error} />

      <div className="mb-6 grid gap-4 md:grid-cols-4">
        <SummaryCard title="Users" value={totals.users} />
        <SummaryCard title="Tasks" value={totals.tasks} />
        <SummaryCard title="Approvals" value={totals.approvals} />
        <SummaryCard title="Documents" value={totals.documents} />
      </div>

      <div className="mb-4 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <select
          value={tenantFilter}
          onChange={(event) => setTenantFilter(event.target.value)}
          className="rounded bg-slate-900 p-2 text-white md:w-80"
        >
          <option value="">All tenants</option>
          {tenants.map((tenant) => (
            <option key={tenant.id} value={tenant.id}>
              {tenant.name}
            </option>
          ))}
        </select>
        <button onClick={load} className="rounded bg-blue-600 px-4 py-2 text-white">
          Refresh Usage
        </button>
      </div>

      <DataTable columns={columns} rows={filteredUsage} />
    </div>
  );
}

function SummaryCard({ title, value }) {
  return (
    <div className="rounded-lg bg-blue-600 p-5 text-white shadow">
      <p className="text-sm opacity-80">{title}</p>
      <p className="text-3xl font-bold">{value}</p>
    </div>
  );
}
