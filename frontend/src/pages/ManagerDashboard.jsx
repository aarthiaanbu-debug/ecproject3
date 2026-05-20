import { useEffect, useState } from "react";
import API from "../services/api";

export default function ManagerDashboard() {

  const [data, setData] = useState({});

  useEffect(() => {

    loadData();

  }, []);

  const loadData = async () => {

    const res = await API.get(
      "/manager/dashboard"
    );

    setData(res.data);
  };

  return (
    <div className="p-5">

      <h1 className="text-2xl mb-5">
        Manager Dashboard
      </h1>

      <div className="bg-slate-800 p-5 rounded">

        <p>
          Team Tasks:
          {data.team_tasks}
        </p>

        <p>
          Approvals Pending:
          {data.approvals_pending}
        </p>

      </div>

    </div>
  );
}