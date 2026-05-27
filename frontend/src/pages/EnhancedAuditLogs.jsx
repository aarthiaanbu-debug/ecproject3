import { useEffect, useState } from "react";
import DataTable from "../components/ui/DataTable";
import FilterBar from "../components/ui/FilterBar";
import PageHeader from "../components/ui/PageHeader";
import { getAuditLogs, getAuditLogsByModule, getAuditLogsByUser } from "../services/api";

export default function EnhancedAuditLogs() {
  const [logs, setLogs] = useState([]);
  const [moduleName, setModuleName] = useState("");
  const [userId, setUserId] = useState("");
  const [selected, setSelected] = useState(null);

  const load = () => getAuditLogs().then((res) => setLogs(res.data || []));

  useEffect(() => {
    load();
  }, []);

  const applyFilters = () => {
    if (moduleName) {
      getAuditLogsByModule(moduleName).then((res) => setLogs(res.data || []));
      return;
    }
    if (userId) {
      getAuditLogsByUser(userId).then((res) => setLogs(res.data || []));
      return;
    }
    load();
  };

  const columns = [
    { key: "id", label: "Log ID" },
    { key: "user_id", label: "User" },
    { key: "module_name", label: "Module" },
    { key: "action_type", label: "Action Type" },
    { key: "record_id", label: "Record ID" },
    { key: "ip_address", label: "IP Address" },
    { key: "created_at", label: "Created At" },
    { key: "actions", label: "Actions", render: (row) => <button onClick={() => setSelected(row)} className="text-blue-600">View Details</button> },
  ];

  return (
    <div className="p-6">
      <PageHeader title="Audit Logs" subtitle="Review detailed backend activity" />
      <FilterBar>
        <input value={moduleName} onChange={(e) => setModuleName(e.target.value)} className="rounded bg-slate-900 p-2 text-white" placeholder="Module name" />
        <input value={userId} onChange={(e) => setUserId(e.target.value)} className="rounded bg-slate-900 p-2 text-white" placeholder="User ID" />
        <button onClick={applyFilters} className="rounded bg-blue-600 px-4 py-2 text-white">Filter</button>
      </FilterBar>
      <DataTable columns={columns} rows={logs} />
      {selected && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
          <div className="max-h-[80vh] w-full max-w-2xl overflow-auto rounded-lg bg-white p-5 text-slate-900">
            <h2 className="text-xl font-bold">Audit Detail #{selected.id}</h2>
            <pre className="mt-4 whitespace-pre-wrap rounded bg-slate-100 p-4 text-sm">
              {JSON.stringify(selected, null, 2)}
            </pre>
            <button onClick={() => setSelected(null)} className="mt-4 rounded bg-blue-600 px-4 py-2 text-white">Close</button>
          </div>
        </div>
      )}
    </div>
  );
}
