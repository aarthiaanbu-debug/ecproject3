import { useEffect, useState } from "react";
import {
  createLeaveRequest,
  getLeaveRequests,
  updateLeaveRequestStatus,
} from "../services/api";

export default function LeaveRequest() {
  const role = (localStorage.getItem("role") || "employee").trim().toLowerCase();
  const canApprove = role === "manager" || role === "admin";

  const [form, setForm] = useState({
    employee_name: "",
    reason: "",
    from_date: "",
    to_date: "",
  });
  const [requests, setRequests] = useState([]);
  const [error, setError] = useState("");

  const load = async () => {
    try {
      const res = await getLeaveRequests();
      setRequests(Array.isArray(res.data) ? res.data : []);
      setError("");
    } catch (err) {
      console.log(err);
      setError("Unable to load leave requests");
    }
  };

  useEffect(() => {
    load();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      await createLeaveRequest(form);
      alert("Leave request submitted to manager");
      setForm({ employee_name: "", reason: "", from_date: "", to_date: "" });
      load();
    } catch (err) {
      console.log(err);
      setError(err.response?.data?.detail || "Unable to submit leave request");
    }
  };

  const updateStatus = async (id, status) => {
    try {
      await updateLeaveRequestStatus(id, status);
      alert(`Leave request ${status}`);
      load();
    } catch (err) {
      console.log(err);
      setError(err.response?.data?.detail || "Unable to update leave request");
    }
  };

  const badgeClass = (status) => {
    if (status === "approved") return "bg-green-500/20 text-green-300";
    if (status === "rejected") return "bg-red-500/20 text-red-300";
    return "bg-yellow-500/20 text-yellow-300";
  };

  return (
    <div className="p-6 text-white w-full">
      <h1 className="text-3xl font-bold mb-6">Leave Requests</h1>
      <p className="mb-4 text-sm text-gray-300">Logged in role: {role}</p>
      {error && <p className="mb-3 text-red-300">{error}</p>}

      <form
        onSubmit={handleSubmit}
        className="bg-white/10 p-6 rounded-2xl backdrop-blur-lg border border-white/10 mb-8"
      >
        <h2 className="text-xl font-semibold mb-4">Apply Leave</h2>
        <div className="grid md:grid-cols-2 gap-4">
          <input
            type="text"
            placeholder="Employee Name"
            value={form.employee_name}
            onChange={(event) =>
              setForm({ ...form, employee_name: event.target.value })
            }
            className="p-3 rounded-xl bg-slate-800 border border-slate-600"
            required
          />
          <input
            type="text"
            placeholder="Reason"
            value={form.reason}
            onChange={(event) =>
              setForm({ ...form, reason: event.target.value })
            }
            className="p-3 rounded-xl bg-slate-800 border border-slate-600"
            required
          />
          <input
            type="date"
            value={form.from_date}
            onChange={(event) =>
              setForm({ ...form, from_date: event.target.value })
            }
            className="p-3 rounded-xl bg-slate-800 border border-slate-600"
            required
          />
          <input
            type="date"
            value={form.to_date}
            onChange={(event) =>
              setForm({ ...form, to_date: event.target.value })
            }
            className="p-3 rounded-xl bg-slate-800 border border-slate-600"
            required
          />
        </div>

        <button
          type="submit"
          className="mt-5 bg-blue-600 hover:bg-blue-700 px-5 py-3 rounded-xl font-bold"
        >
          Apply Leave
        </button>
      </form>

      <div className="grid gap-4">
        {requests.length === 0 && (
          <p className="text-gray-300">No leave requests yet.</p>
        )}

        {requests.map((request) => (
          <div
            key={request.id}
            className="bg-white/10 p-5 rounded-2xl border border-white/10 backdrop-blur-lg"
          >
            <div className="flex justify-between items-start gap-4">
              <div>
                <h2 className="text-xl font-bold">{request.employee_name}</h2>
                <p className="text-gray-300">{request.reason}</p>
                <p className="text-sm text-gray-400 mt-2">
                  {request.from_date} to {request.to_date}
                </p>
              </div>

              {canApprove && String(request.status).toLowerCase() === "pending" && (
                <div className="flex gap-2">
                  <button
                    onClick={() => updateStatus(request.id, "approved")}
                    className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg"
                  >
                    Approve
                  </button>
                  <button
                    onClick={() => updateStatus(request.id, "rejected")}
                    className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg"
                  >
                    Reject
                  </button>
                </div>
              )}
            </div>

            <div className="mt-3">
              <span
                className={`px-3 py-1 rounded-full text-sm font-bold ${badgeClass(
                  request.status
                )}`}
              >
                {request.status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
