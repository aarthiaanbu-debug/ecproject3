import { useEffect, useState } from "react";
import { getApprovals } from "../services/api";

export default function Approval() {
  const [data, setData] = useState([]);

  useEffect(() => {
    getApprovals().then((res) => setData(res.data));
  }, []);

  return (
    <div className="text-white">
      
      {/* Header */}
      <h1 className="text-3xl font-bold mb-6 flex items-center gap-2">
        ✅ Approvals
      </h1>

      {/* Cards */}
      <div className="grid gap-4">
        {data.map((a) => (
          <div
            key={a.id}
            className="bg-white/10 backdrop-blur-lg border border-white/10 p-4 rounded-2xl shadow-lg flex justify-between items-center hover:scale-[1.02] transition"
          >
            <div>
              <p className="text-sm text-gray-300">Task ID</p>
              <p className="text-lg font-bold text-white">#{a.task_id}</p>
            </div>

            <div
              className={`px-3 py-1 rounded-full text-sm font-bold ${
                a.status === "completed"
                  ? "bg-green-500/20 text-green-300"
                  : "bg-yellow-500/20 text-yellow-300"
              }`}
            >
              {a.status}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}