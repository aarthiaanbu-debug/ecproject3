const styles = {
  active: "bg-blue-100 text-blue-700",
  pending: "bg-yellow-100 text-yellow-700",
  breached: "bg-red-100 text-red-700",
  rejected: "bg-red-100 text-red-700",
  escalated: "bg-orange-100 text-orange-700",
  cancelled: "bg-gray-200 text-gray-700",
  resolved: "bg-green-100 text-green-700",
  approved: "bg-green-100 text-green-700",
  completed: "bg-green-100 text-green-700",
  completed_within_sla: "bg-green-100 text-green-700",
  disabled: "bg-gray-200 text-gray-700",
};

export default function StatusBadge({ value }) {
  const normalized = String(value || "pending").toLowerCase();

  return (
    <span
      className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${
        styles[normalized] || "bg-slate-100 text-slate-700"
      }`}
    >
      {String(value || "pending").replaceAll("_", " ")}
    </span>
  );
}
