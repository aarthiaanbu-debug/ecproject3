import { useEffect, useState } from "react";
import { getApprovals, updateApprovalStatus } from "../services/api";

export default function Approval() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    load();
  }, []);

  const load = () => {
    getApprovals()
      .then((res) => setData(Array.isArray(res.data) ? res.data : []))
      .catch(() => setData([]))
      .finally(() => setLoading(false));
  };

  const updateStatus = async (approvalId, status) => {
    await updateApprovalStatus(approvalId, status);
    load();
  };

  const badgeClass = (status) => {
    if (status === "approved") {
      return "bg-green-500/20 text-green-300";
    }

    if (status === "rejected") {
      return "bg-red-500/20 text-red-300";
    }

    return "bg-yellow-500/20 text-yellow-300";
  };

  return (
    <div className="text-white">
      <h1 className="text-3xl font-bold mb-6">Approvals</h1>

      {loading && <p className="text-gray-300">Loading approvals...</p>}

      {!loading && data.length === 0 && (
        <div className="bg-white/10 backdrop-blur-lg border border-white/10 p-5 rounded-2xl text-gray-300">
          No approval requests found.
        </div>
      )}

      <div className="grid gap-4">
        {data.map((approval) => (
          <div
            key={approval.id}
            className="bg-white/10 backdrop-blur-lg border border-white/10 p-4 rounded-2xl shadow-lg flex justify-between items-center hover:scale-[1.02] transition"
          >
            <div>
              <p className="text-sm text-gray-300">Task ID</p>
              <p className="text-lg font-bold text-white">
                #{approval.task_id}
              </p>
            </div>

            <div className="flex items-center gap-2">
              <div
                className={`px-3 py-1 rounded-full text-sm font-bold ${badgeClass(
                  approval.status
                )}`}
              >
                {approval.status || "pending"}
              </div>

              <button
                onClick={() => updateStatus(approval.id, "approved")}
                className="rounded bg-green-600 px-3 py-1 text-sm text-white"
              >
                Approve
              </button>
              <button
                onClick={() => updateStatus(approval.id, "rejected")}
                className="rounded bg-red-600 px-3 py-1 text-sm text-white"
              >
                Reject
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
