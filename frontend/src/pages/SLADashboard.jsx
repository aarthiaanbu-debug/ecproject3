import { useEffect, useMemo, useState } from "react";
import DataTable from "../components/ui/DataTable";
import FilterBar from "../components/ui/FilterBar";
import PageHeader from "../components/ui/PageHeader";
import StatusBadge from "../components/ui/StatusBadge";
import { getActiveSla, getBreachedSla } from "../services/api";

export default function SLADashboard() {
  const [active, setActive] = useState([]);
  const [breached, setBreached] = useState([]);
  const [moduleFilter, setModuleFilter] = useState("");
  const [statusFilter, setStatusFilter] = useState("");

  useEffect(() => {
    getActiveSla().then((res) => setActive(res.data || []));
    getBreachedSla().then((res) => setBreached(res.data || []));
  }, []);

  const rows = useMemo(() => {
    const combined = [...active, ...breached];
    return combined.filter(
      (row) =>
        (!moduleFilter || row.module_name === moduleFilter) &&
        (!statusFilter || row.status === statusFilter)
    );
  }, [active, breached, moduleFilter, statusFilter]);

  const columns = [
    { key: "module_name", label: "Module" },
    { key: "record_id", label: "Record ID" },
    { key: "status", label: "SLA Status", render: (row) => <StatusBadge value={row.status} /> },
    { key: "start_time", label: "Start Time" },
    { key: "due_time", label: "Due Time" },
    { key: "completed_time", label: "Completed Time" },
    { key: "breach_reason", label: "Breach Reason" },
  ];

  return (
    <div className="p-6">
      <PageHeader title="SLA Dashboard" subtitle="Monitor active and breached workflow SLAs" />

      <div className="mb-6 grid gap-4 md:grid-cols-4">
        <Summary title="Active SLA" value={active.length} />
        <Summary title="Breached SLA" value={breached.length} tone="red" />
        <Summary title="Completed Within SLA" value={0} tone="green" />
        <Summary title="Escalated SLA" value={breached.length} tone="orange" />
      </div>

      <FilterBar>
        <select value={moduleFilter} onChange={(e) => setModuleFilter(e.target.value)} className="rounded bg-slate-900 p-2 text-white">
          <option value="">All modules</option>
          <option value="task">Task</option>
          <option value="approval">Approval</option>
        </select>
        <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)} className="rounded bg-slate-900 p-2 text-white">
          <option value="">All statuses</option>
          <option value="active">Active</option>
          <option value="breached">Breached</option>
          <option value="completed_within_sla">Completed</option>
        </select>
      </FilterBar>

      <DataTable columns={columns} rows={rows} />
    </div>
  );
}

function Summary({ title, value, tone = "blue" }) {
  const colors = {
    blue: "bg-blue-600",
    red: "bg-red-600",
    green: "bg-green-600",
    orange: "bg-orange-500",
  };

  return (
    <div className={`${colors[tone]} rounded-lg p-5 text-white shadow`}>
      <p className="text-sm opacity-80">{title}</p>
      <p className="text-3xl font-bold">{value}</p>
    </div>
  );
}
