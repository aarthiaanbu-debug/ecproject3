import { useState } from "react";
import { createTask } from "../services/api";

export default function TaskModal({ onClose, refresh }) {
  const [form, setForm] = useState({
    title: "",
    status: "todo",
  });

  const handleSubmit = async () => {
    if (!form.title) return alert("Enter title");

    await createTask(form);

    refresh(); // reload list
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
      <div className="bg-white p-6 rounded-xl w-96 shadow-lg">
        <h2 className="text-xl font-bold mb-4">Create Task</h2>

        <input
          className="w-full border p-2 mb-3 rounded"
          placeholder="Task Title"
          onChange={(e) =>
            setForm({ ...form, title: e.target.value })
          }
        />

        <select
          className="w-full border p-2 mb-3 rounded"
          onChange={(e) =>
            setForm({ ...form, status: e.target.value })
          }
        >
          <option value="todo">Todo</option>
          <option value="inprogress">In Progress</option>
          <option value="done">Done</option>
        </select>

        <button
          onClick={handleSubmit}
          className="bg-indigo-600 text-white w-full p-2 rounded"
        >
          Create Task
        </button>
      </div>
    </div>
  );
}