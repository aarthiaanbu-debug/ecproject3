import { useEffect, useState } from "react";
import API from "../services";

export default function Analytics() {
  const [data, setData] = useState({});

  useEffect(() => {
    API.get("/analytics").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h2>Analytics</h2>
      <p>Total: {data.total}</p>
      <p>Todo: {data.todo}</p>
      <p>In Progress: {data.inprogress}</p>
      <p>Done: {data.done}</p>
    </div>
  );
}