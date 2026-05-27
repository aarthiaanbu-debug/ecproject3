import { useEffect, useMemo, useState } from "react";
import DataTable from "../components/ui/DataTable";
import ErrorMessage from "../components/ui/ErrorMessage";
import FilterBar from "../components/ui/FilterBar";
import PageHeader from "../components/ui/PageHeader";
import StatusBadge from "../components/ui/StatusBadge";
import {
  createSlaRule,
  disableSlaRule,
  getSlaRules,
  updateSlaRule,
} from "../services/api";

const emptyForm = {
  module_name: "task",
  priority: "high",
  allowed_hours: 24,
  escalation_enabled: true,
  escalation_after_hours: 4,
  is_active: true,
  created_by: 1,
};

export default function SLARules() {
  const [rules, setRules] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState(null);
  const [moduleFilter, setModuleFilter] = useState("");
  const [priorityFilter, setPriorityFilter] = useState("");
  const [error, setError] = useState("");

  const load = () =>
    getSlaRules()
      .then((res) => setRules(res.data || []))
      .catch(() => setError("Unable to load SLA rules"));

  useEffect(() => {
    load();
  }, []);

  const filteredRules = useMemo(
    () =>
      rules.filter(
        (rule) =>
          (!moduleFilter || rule.module_name === moduleFilter) &&
          (!priorityFilter || rule.priority === priorityFilter)
      ),
    [rules, moduleFilter, priorityFilter]
  );

  const submit = async (event) => {
    event.preventDefault();

    if (!form.module_name || !form.priority) {
      setError("Module and priority are required");
      return;
    }

    if (Number(form.allowed_hours) <= 0) {
      setError("Allowed hours must be greater than 0");
      return;
    }

    if (form.escalation_enabled && Number(form.escalation_after_hours) <= 0) {
      setError("Escalation hours must be greater than 0");
      return;
    }

    const payload = {
      ...form,
      allowed_hours: Number(form.allowed_hours),
      escalation_after_hours: Number(form.escalation_after_hours),
    };

    try {
      if (editingId) {
        await updateSlaRule(editingId, payload);
      } else {
        await createSlaRule(payload);
      }
      setForm(emptyForm);
      setEditingId(null);
      setError("");
      load();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to save SLA rule");
    }
  };

  const edit = (rule) => {
    setEditingId(rule.id);
    setForm({
      module_name: rule.module_name,
      priority: rule.priority,
      allowed_hours: rule.allowed_hours,
      escalation_enabled: Boolean(rule.escalation_enabled),
      escalation_after_hours: rule.escalation_after_hours || 0,
      is_active: Boolean(rule.is_active),
      created_by: rule.created_by || 1,
    });
  };

  const columns = [
    { key: "id", label: "Rule ID" },
    { key: "module_name", label: "Module" },
    { key: "priority", label: "Priority" },
    { key: "allowed_hours", label: "Allowed Hours" },
    {
      key: "escalation_enabled",
      label: "Escalation",
      render: (rule) => (rule.escalation_enabled ? "Yes" : "No"),
    },
    { key: "escalation_after_hours", label: "Escalation After" },
    {
      key: "is_active",
      label: "Status",
      render: (rule) => <StatusBadge value={rule.is_active ? "active" : "disabled"} />,
    },
    {
      key: "actions",
      label: "Actions",
      render: (rule) => (
        <div className="flex gap-2">
          <button onClick={() => edit(rule)} className="text-blue-600">
            Edit
          </button>
          <button onClick={() => disableSlaRule(rule.id).then(load)} className="text-red-600">
            Disable
          </button>
        </div>
      ),
    },
  ];

  return (
    <div className="p-6">
      <PageHeader title="SLA Rules" subtitle="Create and manage workflow SLA policies" />
      <ErrorMessage message={error} />

      <FilterBar>
        <select value={moduleFilter} onChange={(e) => setModuleFilter(e.target.value)} className="rounded bg-slate-900 p-2 text-white">
          <option value="">All modules</option>
          <option value="task">Task</option>
          <option value="approval">Approval</option>
        </select>
        <select value={priorityFilter} onChange={(e) => setPriorityFilter(e.target.value)} className="rounded bg-slate-900 p-2 text-white">
          <option value="">All priorities</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </FilterBar>

      <form onSubmit={submit} className="mb-6 grid gap-3 rounded-lg bg-white/10 p-4 md:grid-cols-4">
        <select value={form.module_name} onChange={(e) => setForm({ ...form, module_name: e.target.value })} className="rounded bg-slate-900 p-2 text-white">
          <option value="task">Task</option>
          <option value="approval">Approval</option>
        </select>
        <select value={form.priority} onChange={(e) => setForm({ ...form, priority: e.target.value })} className="rounded bg-slate-900 p-2 text-white">
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
        <input type="number" value={form.allowed_hours} onChange={(e) => setForm({ ...form, allowed_hours: e.target.value })} className="rounded bg-slate-900 p-2 text-white" placeholder="Allowed hours" />
        <input type="number" value={form.escalation_after_hours} onChange={(e) => setForm({ ...form, escalation_after_hours: e.target.value })} className="rounded bg-slate-900 p-2 text-white" placeholder="Escalation hours" />
        <label className="text-white">
          <input type="checkbox" checked={form.escalation_enabled} onChange={(e) => setForm({ ...form, escalation_enabled: e.target.checked })} /> Escalation enabled
        </label>
        <label className="text-white">
          <input type="checkbox" checked={form.is_active} onChange={(e) => setForm({ ...form, is_active: e.target.checked })} /> Active
        </label>
        <button className="rounded bg-blue-600 px-4 py-2 text-white md:col-span-2">
          {editingId ? "Update Rule" : "Create Rule"}
        </button>
      </form>

      <DataTable columns={columns} rows={filteredRules} />
    </div>
  );
}
