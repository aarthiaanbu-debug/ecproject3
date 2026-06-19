import { useEffect, useState } from "react";
import { getChannelTasks } from "../api/api";

export default function ChannelTasks() {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    const res = await getChannelTasks(1);
    setTasks(res.data.items || res.data);
  };

  return (
    <div className="p-6 text-white">
      <h1 className="text-3xl font-bold mb-5">
        Channel Tasks
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