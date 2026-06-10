import { useEffect, useState } from "react";
import { createApproval, createTask, getTasks } from "../services/api";

export default function Tasks() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");

  const load = async () => {
    try {
      const res = await getTasks();
      setTasks(Array.isArray(res.data) ? res.data : res.data?.data || []);
      setError("");
    } catch (err) {
      console.log(err);
      setError("Unable to load tasks");
      setTasks([]);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const addTask = async () => {
    if (!title.trim()) {
      setError("Enter a task title");
      return;
    }

    if (!description.trim()) {
      setError("Enter a task description");
      return;
    }

    try {
      await createTask({
        title: title.trim(),
        description: description.trim(),
      });
      setTitle("");
      setDescription("");
      await load();
    } catch (err) {
      console.log(err);
      setError(err.response?.data?.detail || "Unable to create task");
    }
  };

  const sendForApproval = async (taskId) => {
    try {
      await createApproval(taskId);
      setError("");
      alert("Task sent for approval");
    } catch (err) {
      console.log(err);
      setError(err.response?.data?.detail || "Unable to create approval");
    }
  };

  return (
    <div className="text-white">
      <h1 className="text-3xl font-bold mb-4">Tasks</h1>
      {error && <p className="text-red-300 mb-3">{error}</p>}

      <div className="grid gap-3 mb-6 md:grid-cols-[1fr_2fr_auto]">
        <input
          className="p-2 rounded bg-white/10 text-white border border-white/20"
          placeholder="Task title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />

        <input
          className="p-2 rounded bg-white/10 text-white border border-white/20"
          placeholder="Task description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />

        <button onClick={addTask} className="btn btn-primary">
          + Create
        </button>
      </div>

      <div className="grid gap-3">
        {tasks.length === 0 && <p className="text-gray-300">No tasks found</p>}

        {tasks.map((task) => (
          <div key={task.id} className="card p-4 flex justify-between gap-4">
            <div>
              <p className="font-semibold">{task.title}</p>
              <p className="text-sm text-gray-300">{task.description}</p>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={() => sendForApproval(task.id)}
                className="rounded bg-amber-500 px-3 py-1 text-sm text-white"
              >
                Send for Approval
              </button>
              <span className="text-purple-300">{task.status}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
