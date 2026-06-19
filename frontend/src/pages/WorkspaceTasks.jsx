import { useEffect, useState } from "react";
import {
  createWorkspaceTask,
  getWorkspaceTasks,
} from "../api/api";

export default function WorkspaceTasks() {
  const [tasks, setTasks] = useState([]);

  const loadTasks = async () => {
    const res = await getWorkspaceTasks(1);
    setTasks(res.data.items || res.data);
  };

  useEffect(() => {
    loadTasks();
  }, []);

  return (
    <div className="p-6 text-white">
      <h1 className="text-3xl font-bold mb-5">
        Workspace Tasks
      </h1>

      {tasks.map((task) => (
        <div
          key={task.id}
          className="bg-white text-black p-4 rounded mb-3"
        >
          <h2>{task.title}</h2>
          <p>{task.description}</p>
        </div>
      ))}
    </div>
  );
}