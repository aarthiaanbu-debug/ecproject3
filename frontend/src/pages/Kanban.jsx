import { useEffect, useState } from "react";
import { getKanban, updateTask } from "../services/api";

export default function Kanban() {

  const [board, setBoard] = useState({
    todo: [],
    inprogress: [],
    done: [],
  });

  useEffect(() => {
    load();
  }, []);

  const load = async () => {
    const res = await getKanban();

    setBoard({
      todo: res.data?.todo || [],
      inprogress: res.data?.inprogress || [],
      done: res.data?.done || [],
    });
  };

  const move = async (id, status) => {
    await updateTask(id, status);
    load();
  };

  const Column = ({ title, items, color }) => (
    <div className="bg-white/10 p-4 rounded-2xl min-h-[500px]">

      <h2 className="font-bold mb-4">{title}</h2>

      {items.map((t) => (
        <div key={t.id} className="bg-black/20 p-3 mb-3 rounded-xl">

          <p>{t.title}</p>

          <select
            value={t.status}
            onChange={(e) => move(t.id, e.target.value)}
            className="mt-2 text-black"
          >
            <option value="todo">Todo</option>
            <option value="inprogress">In Progress</option>
            <option value="done">Done</option>
          </select>

        </div>
      ))}

    </div>
  );

  return (
    <div className="grid md:grid-cols-3 gap-4 p-4">

      <Column title="Todo" items={board.todo} />
      <Column title="In Progress" items={board.inprogress} />
      <Column title="Done" items={board.done} />

    </div>
  );
}