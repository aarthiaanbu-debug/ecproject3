import { useEffect, useState } from "react";
import API from "../services/api";

export default function AdminDashboard() {

  const [data, setData] = useState({});

  useEffect(() => {

    loadData();

  }, []);

  const loadData = async () => {

    const res = await API.get(
      "/admin/dashboard"
    );

    setData(res.data);
  };

  return (
    <div className="p-5">

      <h1 className="text-2xl mb-5">
        Admin Dashboard
      </h1>

      <div className="bg-slate-800 p-5 rounded">

        <p>Users: {data.users}</p>

        <p>Documents: {data.documents}</p>

        <p>
          Active Tasks:
          {data.active_tasks}
        </p>

      </div>

    </div>
  );
}