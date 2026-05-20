import { useEffect, useState } from "react";
import API from "../services/api";

export default function EmployeeDashboard() {

  const [data, setData] = useState({});

  useEffect(() => {

    loadData();

  }, []);

  const loadData = async () => {

    const res = await API.get(
      "/employee/dashboard"
    );

    setData(res.data);
  };

  return (
    <div className="p-5">

      <h1 className="text-2xl mb-5">
        Employee Dashboard
      </h1>

      <div className="bg-slate-800 p-5 rounded">

        <p>Tasks: {data.tasks}</p>

        <p>
          Pending Requests:
          {data.pending_requests}
        </p>

      </div>

    </div>
  );
}