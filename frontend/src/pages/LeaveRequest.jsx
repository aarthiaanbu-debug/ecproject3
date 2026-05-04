import { useState } from "react";
import toast from "react-hot-toast";

export default function LeaveRequest() {
  const [form, setForm] = useState({
    name: "",
    reason: "",
    from: "",
    to: "",
  });

  const [requests, setRequests] = useState([]);

  const handleSubmit = (e) => {
    e.preventDefault();

    const newRequest = {
      id: Date.now(),
      ...form,
      status: "Pending",
    };

    setRequests([...requests, newRequest]);

    toast.success("Leave Request Submitted ✅");

    setForm({
      name: "",
      reason: "",
      from: "",
      to: "",
    });
  };

  const updateStatus = (id, status) => {
    const updated = requests.map((r) =>
      r.id === id ? { ...r, status } : r
    );

    setRequests(updated);

    toast.success(`Request ${status}`);
  };

  return (
    <div className="p-6 text-white w-full">

      <h1 className="text-3xl font-bold mb-6">
        🏖 Leave Request
      </h1>

      {/* FORM */}
      <form
        onSubmit={handleSubmit}
        className="bg-white/10 p-6 rounded-2xl backdrop-blur-lg border border-white/10 mb-8"
      >
        <div className="grid md:grid-cols-2 gap-4">

          <input
            type="text"
            placeholder="Employee Name"
            value={form.name}
            onChange={(e) =>
              setForm({ ...form, name: e.target.value })
            }
            className="p-3 rounded-xl bg-slate-800 border border-slate-600"
            required
          />

          <input
            type="text"
            placeholder="Reason"
            value={form.reason}
            onChange={(e) =>
              setForm({ ...form, reason: e.target.value })
            }
            className="p-3 rounded-xl bg-slate-800 border border-slate-600"
            required
          />

          <input
            type="date"
            value={form.from}
            onChange={(e) =>
              setForm({ ...form, from: e.target.value })
            }
            className="p-3 rounded-xl bg-slate-800 border border-slate-600"
            required
          />

          <input
            type="date"
            value={form.to}
            onChange={(e) =>
              setForm({ ...form, to: e.target.value })
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

      {/* REQUEST LIST */}
      <div className="grid gap-4">
        {requests.map((req) => (
          <div
            key={req.id}
            className="bg-white/10 p-5 rounded-2xl border border-white/10 backdrop-blur-lg"
          >
            <div className="flex justify-between items-start">

              <div>
                <h2 className="text-xl font-bold">
                  {req.name}
                </h2>

                <p className="text-gray-300">
                  {req.reason}
                </p>

                <p className="text-sm text-gray-400 mt-2">
                  {req.from} → {req.to}
                </p>
              </div>

              <div className="flex gap-2">

                <button
                  onClick={() =>
                    updateStatus(req.id, "Approved")
                  }
                  className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg"
                >
                  Approve
                </button>

                <button
                  onClick={() =>
                    updateStatus(req.id, "Rejected")
                  }
                  className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg"
                >
                  Reject
                </button>
              </div>
            </div>

            <div className="mt-3">
              <span
                className={`px-3 py-1 rounded-full text-sm font-bold ${
                  req.status === "Approved"
                    ? "bg-green-500/20 text-green-300"
                    : req.status === "Rejected"
                    ? "bg-red-500/20 text-red-300"
                    : "bg-yellow-500/20 text-yellow-300"
                }`}
              >
                {req.status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}