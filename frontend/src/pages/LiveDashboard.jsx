import { useEffect, useState } from "react";
import { getAnalytics } from "../services/api";

export default function LiveDashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    load();

    const ws = new WebSocket("ws://127.0.0.1:8000/ws/kanban");

    ws.onmessage = () => {
      load(); // live refresh
    };

    return () => ws.close();
  }, []);

  const load = async () => {
    const res = await getAnalytics();
    setData(res.data);
  };

  if (!data) return <div className="text-white">Loading...</div>;

  return (
    <div className="grid grid-cols-4 gap-4 text-white">
      <Card title="Total" value={data.total} />
      <Card title="Todo" value={data.todo} />
      <Card title="Progress" value={data.inprogress} />
      <Card title="Done" value={data.done} />
    </div>
  );
}

function Card({ title, value }) {
  return (
    <div className="bg-white/10 p-6 rounded-2xl">
      <h2>{title}</h2>
      <p className="text-3xl font-bold">{value}</p>
    </div>
  );
}