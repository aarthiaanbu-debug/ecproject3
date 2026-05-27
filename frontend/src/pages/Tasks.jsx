import { useEffect, useState } from "react";
import { getTasks, createTask, deleteTask } from "../services/api";

export default function Tasks() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
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

    try {
      await createTask({ title, description: "New Task" });
      setTitle("");
      load();
    } catch (err) {
      console.log(err);
      setError("Unable to create task");
    }
  };

  return (
    <div className="text-white">
      <h1 className="text-3xl font-bold mb-4">📌 Tasks</h1>
      {error && <p className="text-red-300 mb-3">{error}</p>}

      <div className="flex gap-2 mb-6">
        <input
          className="p-2 rounded bg-white/10 text-white border border-white/20"
          placeholder="Task title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />

        <button onClick={addTask} className="btn btn-primary">
          + Create
        </button>
      </div>

      <div className="grid gap-3">
        {tasks.length === 0 && <p className="text-gray-300">No tasks found</p>}

        {tasks.map((t) => (
          <div key={t.id} className="card p-4 flex justify-between">
            <span>{t.title}</span>
            <span className="text-purple-300">{t.status}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
