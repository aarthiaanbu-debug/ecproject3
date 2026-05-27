import { useEffect, useState } from "react";
import DataTable from "../components/ui/DataTable";
import ErrorMessage from "../components/ui/ErrorMessage";
import PageHeader from "../components/ui/PageHeader";
import StatusBadge from "../components/ui/StatusBadge";
import UserSelectDropdown from "../components/ui/UserSelectDropdown";
import {
  cancelApprovalDelegation,
  createApprovalDelegation,
  getActiveApprovalDelegations,
} from "../services/api";

export default function ApprovalDelegations() {
  const [rows, setRows] = useState([]);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    delegator_id: 1,
    delegatee_id: "",
    start_date: "",
    end_date: "",
    reason: "",
  });

  const load = () => getActiveApprovalDelegations().then((res) => setRows(res.data || []));

  useEffect(() => {
    load();
  }, []);

  const submit = async (event) => {
    event.preventDefault();
    if (!form.delegatee_id || !form.start_date || !form.end_date || !form.reason.trim()) {
      setError("Delegatee, dates, and reason are required");
      return;
    }

    if (new Date(form.end_date) <= new Date(form.start_date)) {
      setError("End date must be after start date");
      return;
    }

    try {
      await createApprovalDelegation({
        ...form,
        delegatee_id: Number(form.delegatee_id),
        start_date: new Date(form.start_date).toISOString(),
        end_date: new Date(form.end_date).toISOString(),
      });
      setForm({ delegator_id: 1, delegatee_id: "", start_date: "", end_date: "", reason: "" });
      setError("");
      load();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to create delegation");
    }
  };

  const columns = [
    { key: "delegator_id", label: "Delegator" },
    { key: "delegatee_id", label: "Delegatee" },
    { key: "start_date", label: "Start Date" },
    { key: "end_date", label: "End Date" },
    { key: "reason", label: "Reason" },
    { key: "status", label: "Status", render: (row) => <StatusBadge value={row.is_active ? "active" : "cancelled"} /> },
    { key: "actions", label: "Actions", render: (row) => <button onClick={() => cancelApprovalDelegation(row.id).then(load)} className="text-red-600">Cancel</button> },
  ];

  return (
    <div className="p-6">
      <PageHeader title="Approval Delegations" subtitle="Delegate approval responsibility for planned absence" />
      <ErrorMessage message={error} />
      <form onSubmit={submit} className="mb-6 grid gap-3 rounded-lg bg-white/10 p-4 md:grid-cols-5">
        <UserSelectDropdown value={form.delegatee_id} onChange={(value) => setForm({ ...form, delegatee_id: value })} />
        <input type="datetime-local" value={form.start_date} onChange={(e) => setForm({ ...form, start_date: e.target.value })} className="rounded bg-slate-900 p-2 text-white" />
        <input type="datetime-local" value={form.end_date} onChange={(e) => setForm({ ...form, end_date: e.target.value })} className="rounded bg-slate-900 p-2 text-white" />
        <textarea value={form.reason} onChange={(e) => setForm({ ...form, reason: e.target.value })} className="rounded bg-slate-900 p-2 text-white" placeholder="Reason" />
        <button className="rounded bg-blue-600 px-4 py-2 text-white">Create</button>
      </form>
      <DataTable columns={columns} rows={rows} />
    </div>
  );
}
