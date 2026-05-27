import { useEffect, useState } from "react";
import DataTable from "../components/ui/DataTable";
import ErrorMessage from "../components/ui/ErrorMessage";
import PageHeader from "../components/ui/PageHeader";
import StatusBadge from "../components/ui/StatusBadge";
import UserSelectDropdown from "../components/ui/UserSelectDropdown";
import {
  cancelApprovalEscalation,
  createApprovalEscalation,
  getApprovalEscalations,
  resolveApprovalEscalation,
} from "../services/api";

export default function ApprovalEscalations() {
  const [rows, setRows] = useState([]);
  const [form, setForm] = useState({ approval_id: "", escalated_to: "", reason: "" });
  const [error, setError] = useState("");

  const load = () => getApprovalEscalations().then((res) => setRows(res.data || []));

  useEffect(() => {
    load();
  }, []);

  const submit = async (event) => {
    event.preventDefault();
    if (!form.approval_id || !form.escalated_to || !form.reason.trim()) {
      setError("Approval ID, escalated user, and reason are required");
      return;
    }

    try {
      await createApprovalEscalation({
        approval_id: Number(form.approval_id),
        escalated_to: Number(form.escalated_to),
        reason: form.reason,
      });
      setForm({ approval_id: "", escalated_to: "", reason: "" });
      setError("");
      load();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to escalate approval");
    }
  };

  const columns = [
    { key: "id", label: "Escalation ID" },
    { key: "approval_id", label: "Approval ID" },
    { key: "escalated_from", label: "Escalated From" },
    { key: "escalated_to", label: "Escalated To" },
    { key: "reason", label: "Reason" },
    { key: "escalation_level", label: "Level" },
    { key: "status", label: "Status", render: (row) => <StatusBadge value={row.status} /> },
    { key: "escalated_at", label: "Escalated At" },
    {
      key: "actions",
      label: "Actions",
      render: (row) => (
        <div className="flex gap-2">
          <button onClick={() => resolveApprovalEscalation(row.id).then(load)} className="text-green-600">Resolve</button>
          <button onClick={() => cancelApprovalEscalation(row.id).then(load)} className="text-red-600">Cancel</button>
        </div>
      ),
    },
  ];

  return (
    <div className="p-6">
      <PageHeader title="Approval Escalations" subtitle="Escalate and resolve delayed approvals" />
      <ErrorMessage message={error} />
      <form onSubmit={submit} className="mb-6 grid gap-3 rounded-lg bg-white/10 p-4 md:grid-cols-4">
        <input value={form.approval_id} onChange={(e) => setForm({ ...form, approval_id: e.target.value })} className="rounded bg-slate-900 p-2 text-white" placeholder="Approval ID" />
        <UserSelectDropdown value={form.escalated_to} onChange={(value) => setForm({ ...form, escalated_to: value })} />
        <textarea value={form.reason} onChange={(e) => setForm({ ...form, reason: e.target.value })} className="rounded bg-slate-900 p-2 text-white" placeholder="Reason" />
        <button className="rounded bg-orange-500 px-4 py-2 text-white">Escalate</button>
      </form>
      <DataTable columns={columns} rows={rows} />
    </div>
  );
}
