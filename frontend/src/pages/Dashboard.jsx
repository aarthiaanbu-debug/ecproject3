import { useEffect, useState } from "react";
import { getAnalytics } from "../services/api";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    getAnalytics().then((res) => setData(res.data));
  }, []);

  if (!data) return <div className="text-white">Loading...</div>;

  const chartData = [
    { name: "Todo", value: data.todo || 0 },
    { name: "In Progress", value: data.inprogress || 0 },
    { name: "Done", value: data.done || 0 },
  ];

  const COLORS = ["#60a5fa", "#facc15", "#4ade80"];

  return (
    <div className="text-white space-y-6">

      <h1 className="text-3xl font-bold">📊 Dashboard Analytics</h1>

      {/* CARDS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

        <div className="bg-white/10 p-4 rounded-2xl">
          Total Tasks: <span className="font-bold">{data.total}</span>
        </div>

        <div className="bg-white/10 p-4 rounded-2xl">
          In Progress: <span className="font-bold">{data.inprogress}</span>
        </div>

        <div className="bg-white/10 p-4 rounded-2xl">
          Completed: <span className="font-bold">{data.done}</span>
        </div>

      </div>

      {/* CHART */}
      <div className="bg-white/10 p-6 rounded-2xl h-[350px]">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={chartData}
              dataKey="value"
              outerRadius={120}
              label
            >
              {chartData.map((entry, index) => (
                <Cell key={index} fill={COLORS[index]} />
              ))}
            </Pie>

            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>

    </div>
  );
}