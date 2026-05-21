import {
  Bar,
  BarChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

export default function AnalyticsChart({ data }) {
  const chart = [
    { name: "Todo", value: data?.todo || 0 },
    { name: "Progress", value: data?.inprogress || 0 },
    { name: "Done", value: data?.done || 0 },
    { name: "Pending Approvals", value: data?.approvals_pending || 0 },
  ];

  return (
    <div className="bg-white/10 p-5 rounded-2xl mt-6">
      <h2 className="text-xl font-bold mb-4">Analytics</h2>

      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={chart}>
          <XAxis dataKey="name" stroke="#cbd5e1" />
          <YAxis stroke="#cbd5e1" allowDecimals={false} />
          <Tooltip />
          <Bar dataKey="value" fill="#22d3ee" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
