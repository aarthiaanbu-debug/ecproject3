import { useEffect, useState } from "react";
import { getAuditLogs } from "../services/api";

export default function AuditLogs() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    getAuditLogs().then(res => setLogs(res.data));
  }, []);

  return (
    <div className="text-white p-5">
      <h1 className="text-2xl mb-4">Audit Logs</h1>

      {logs.map((log) => (
        <div key={log.id} className="bg-white/10 p-3 mb-2 rounded">
          {log.action} - {log.created_at}
        </div>
      ))}
    </div>
  );
}