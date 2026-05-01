import { useEffect, useState } from "react";
import { getTasks, createTask, deleteTask } from "../services/api";

export default function Tasks() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");

  const load = async () => {
    const res = await getTasks();
    setTasks(res.data);
  };

  useEffect(() => {
    load();
  }, []);

  const addTask = async () => {
    await createTask({ title, description: "New Task" });
    setTitle("");
    load();
  };

  return (
    <div className="text-white">
      <h1 className="text-3xl font-bold mb-4">📌 Tasks</h1>

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