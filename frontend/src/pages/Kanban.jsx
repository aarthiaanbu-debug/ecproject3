import { useEffect, useState } from "react";
import { getKanban, updateTask } from "../services/api";

export default function Kanban() {
  const [board, setBoard] = useState({
    todo: [],
    inprogress: [],
    done: [],
  });

  const load = async () => {
    try {
      const res = await getKanban();

      console.log("KANBAN DATA:", res.data); // 🔥 debug

      setBoard({
        todo: res.data?.todo || [],
        inprogress: res.data?.inprogress || [],
        done: res.data?.done || [],
      });
    } catch (err) {
      console.error("Kanban load error:", err);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const move = async (id, status) => {
    try {
      await updateTask(id, status);
      load();
    } catch (err) {
      console.error("Move error:", err);
    }
  };

  const Column = ({ title, color, items }) => {
    const colorMap = {
      blue: "bg-blue-100",
      yellow: "bg-yellow-100",
      green: "bg-green-100",
    };

    return (
      <div className={`${colorMap[color]} p-4 rounded-2xl shadow-lg min-h-[500px]`}>
        
        <h2 className="font-bold text-lg mb-4 text-gray-700">
          {title}
        </h2>

        {items.length === 0 && (
          <div className="text-gray-400 text-sm text-center mt-10">
            No tasks
          </div>
        )}

        {items.map((t) => (
          <div
            key={t.id}
            className="bg-white p-3 mb-3 rounded-xl shadow border hover:shadow-md transition"
          >
            <p className="font-medium text-gray-800">{t.title}</p>

            <select
              className="mt-2 text-sm border rounded px-2 py-1"
              value={t.status}
              onChange={(e) => move(t.id, e.target.value)}
            >
              <option value="todo">Todo</option>
              <option value="inprogress">In Progress</option>
              <option value="done">Done</option>
            </select>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 p-4">
      <Column title="Todo" color="blue" items={board.todo} />
      <Column title="In Progress" color="yellow" items={board.inprogress} />
      <Column title="Done" color="green" items={board.done} />
    </div>
  );
}