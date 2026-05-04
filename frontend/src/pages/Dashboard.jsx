import { useEffect, useState } from "react";
import { getAnalytics } from "../services/api";

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    getAnalytics().then((res) => setData(res.data));
  }, []);

  if (!data) return <div className="text-white">Loading...</div>;

  const {
    total,
    todo,
    inprogress,
    done,
    avg_completion_time,
    overdue,
    due_today,
    top_performer
  } = data;

  const percent = (value) => {
    if (total === 0) return 0;
    return Math.round((value / total) * 100);
  };

  return (
    <div className="text-white">
      <h1 className="text-3xl font-bold mb-6">📊 Dashboard Analytics</h1>

      {/* CARDS */}
      <div className="grid md:grid-cols-4 gap-6 mb-8">

        <div className="card p-6">
          <h2>Total Tasks</h2>
          <p className="text-4xl font-bold text-purple-300">{total}</p>
        </div>

        <div className="card p-6">
          <h2>Todo</h2>
          <p className="text-4xl font-bold text-blue-300">{todo}</p>
        </div>

        <div className="card p-6">
          <h2>In Progress</h2>
          <p className="text-4xl font-bold text-yellow-300">{inprogress}</p>
        </div>

        <div className="card p-6">
          <h2>Done</h2>
          <p className="text-4xl font-bold text-green-300">{done}</p>
        </div>

      </div>

      {/* 📈 TASK DISTRIBUTION */}
      <div className="card p-6 mb-8">
        <h2 className="text-xl mb-4">📈 Task Distribution</h2>

        <div className="space-y-4">

          <div>
            <p>Todo ({percent(todo)}%)</p>
            <div className="w-full bg-gray-700 rounded h-3">
              <div
                className="bg-blue-400 h-3 rounded"
                style={{ width: `${percent(todo)}%` }}
              ></div>
            </div>
          </div>

          <div>
            <p>In Progress ({percent(inprogress)}%)</p>
            <div className="w-full bg-gray-700 rounded h-3">
              <div
                className="bg-yellow-400 h-3 rounded"
                style={{ width: `${percent(inprogress)}%` }}
              ></div>
            </div>
          </div>

          <div>
            <p>Done ({percent(done)}%)</p>
            <div className="w-full bg-gray-700 rounded h-3">
              <div
                className="bg-green-400 h-3 rounded"
                style={{ width: `${percent(done)}%` }}
              ></div>
            </div>
          </div>

        </div>
      </div>

      {/* 🚀 PERFORMANCE INSIGHTS */}
      <div className="card p-6">
        <h2 className="text-xl mb-4">🚀 Performance Insights</h2>

        <ul className="space-y-2 text-lg">

          {done === total && (
            <li className="text-green-400">
              ✅ All tasks completed — Excellent performance!
            </li>
          )}

          {inprogress > 0 && (
            <li className="text-yellow-400">
              ⚠️ Tasks are in progress — Keep going!
            </li>
          )}

          {todo > done && (
            <li className="text-red-400">
              🔴 Many tasks pending — Need attention!
            </li>
          )}

          {done > 0 && done < total && (
            <li className="text-blue-400">
              👍 Good progress — Tasks are being completed
            </li>
          )}

        </ul>

        {/* 🔥 NEW METRICS (ADDED WITHOUT CHANGING OLD CODE) */}
        <div className="mt-6 grid md:grid-cols-2 gap-4 text-sm">

          <div className="bg-white/5 p-3 rounded">
            ⏱ Avg Completion Time:{" "}
            <span className="text-purple-300 font-bold">
              {avg_completion_time || "N/A"}
            </span>
          </div>

          <div className="bg-white/5 p-3 rounded">
            ⏰ Overdue Tasks:{" "}
            <span className="text-red-400 font-bold">
              {overdue || 0}
            </span>
          </div>

          <div className="bg-white/5 p-3 rounded">
            📅 Tasks Due Today:{" "}
            <span className="text-yellow-300 font-bold">
              {due_today || 0}
            </span>
          </div>

          <div className="bg-white/5 p-3 rounded">
            🏆 Top Performer:{" "}
            <span className="text-green-300 font-bold">
              {top_performer || "N/A"}
            </span>
          </div>

        </div>

      </div>

    </div>
  );
}