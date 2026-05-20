import { useEffect, useState } from "react";
import { getAISummary } from "../services/api";

export default function AIInsights() {
  const [data, setData] = useState(null);

  useEffect(() => {
    getAISummary().then(res => setData(res.data));
  }, []);

  if (!data) return <div className="text-white">Loading...</div>;

  return (
    <div className="text-white p-5">
      <h1 className="text-2xl mb-4">AI Insights</h1>

      <div className="bg-white/10 p-4 rounded">
        <p>🔥 High Priority Tasks: {data.high_priority}</p>
        <p>⚠ Delay Risk: {data.delay_risk}</p>
      </div>
    </div>
  );
}