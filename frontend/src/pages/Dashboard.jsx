import { useEffect, useState } from "react";

import {
  getAnalytics,
  getNotifications,
  markNotificationRead,
  getDocuments,
  getComments,
  addComment,
} from "../services/api";

export default function Dashboard() {

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  const [notifications, setNotifications] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [comments, setComments] = useState({});
  const [commentText, setCommentText] = useState({});

  // =========================
  // LOAD DASHBOARD
  // =========================
  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      setLoading(true);

      // ANALYTICS
      const analyticsRes = await getAnalytics();
      setData(analyticsRes.data);

      // NOTIFICATIONS
      const notificationRes = await getNotifications();
      setNotifications(notificationRes.data || []);

      // DOCUMENTS
      const documentRes = await getDocuments();

      const docs = Array.isArray(documentRes.data)
        ? documentRes.data
        : documentRes.data?.documents || [];

      setDocuments(docs);

      // COMMENTS
      const tempComments = {};

      for (const doc of docs) {
        if (!doc.task_id) {
          tempComments[doc.id] = [];
          continue;
        }

        try {
          const res = await getComments(doc.task_id);
          tempComments[doc.id] = res.data || [];
        } catch {
          tempComments[doc.id] = [];
        }
      }

      setComments(tempComments);

    } catch (err) {
      console.log("Dashboard Error:", err);

      setData({
        total: 0,
        todo: 0,
        inprogress: 0,
        done: 0,
        avg_completion_time: 0,
        overdue: 0,
        due_today: 0,
        top_performer: "N/A",
      });

    } finally {
      setLoading(false);
    }
  };

  // =========================
  // NOTIFICATION READ
  // =========================
  const handleRead = async (id) => {
    try {
      await markNotificationRead(id);
      loadDashboard();
    } catch (err) {
      console.log(err);
    }
  };

  // =========================
  // COMMENT ADD (FIXED)
  // =========================
  const handleComment = async (docId, taskId) => {
    if (!commentText[docId]) return;

    try {
      await addComment({
        task_id: taskId,
        content: commentText[docId],
      });

      setCommentText((prev) => ({
        ...prev,
        [docId]: "",
      }));

      loadDashboard();

    } catch (err) {
      console.log(err);
    }
  };

  // =========================
  // LOADING UI
  // =========================
  if (loading || !data) {
    return (
      <div className="h-screen flex items-center justify-center text-white text-xl">
        Loading Dashboard...
      </div>
    );
  }

  const {
    total,
    todo,
    inprogress,
    done,
    avg_completion_time,
    overdue,
    due_today,
    top_performer
  } = data;

  const percent = (value) => {
    if (total === 0) return 0;
    return Math.round((value / total) * 100);
  };

  return (
    <div className="text-white p-6">

      {/* HEADER */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold">📊 Dashboard Analytics</h1>
        <p className="text-gray-400 mt-2">Enterprise Workflow Monitoring</p>
      </div>

      {/* CARDS */}
      <div className="grid md:grid-cols-4 gap-6 mb-8">

        <div className="bg-gradient-to-r from-purple-500 to-indigo-600 p-6 rounded-3xl">
          <h2>Total Tasks</h2>
          <p className="text-3xl font-bold">{total}</p>
        </div>

        <div className="bg-gradient-to-r from-blue-500 to-cyan-500 p-6 rounded-3xl">
          <h2>Todo</h2>
          <p className="text-3xl font-bold">{todo}</p>
        </div>

        <div className="bg-gradient-to-r from-yellow-500 to-orange-500 p-6 rounded-3xl">
          <h2>In Progress</h2>
          <p className="text-3xl font-bold">{inprogress}</p>
        </div>

        <div className="bg-gradient-to-r from-green-500 to-emerald-500 p-6 rounded-3xl">
          <h2>Done</h2>
          <p className="text-3xl font-bold">{done}</p>
        </div>

      </div>

      {/* TASK DISTRIBUTION */}
      <div className="bg-white/10 p-6 rounded-3xl mb-8">
        <h2 className="text-xl mb-4">Task Distribution</h2>
        <p>Todo: {percent(todo)}%</p>
        <p>Progress: {percent(inprogress)}%</p>
        <p>Done: {percent(done)}%</p>
      </div>

      {/* PERFORMANCE */}
      <div className="bg-white/10 p-6 rounded-3xl mb-8">
        <h2 className="text-xl mb-4">Performance</h2>
        <p>⏱ Avg Time: {avg_completion_time}</p>
        <p>⏰ Overdue: {overdue}</p>
        <p>📅 Due Today: {due_today}</p>
        <p>🏆 Top: {top_performer}</p>
      </div>

      {/* NOTIFICATIONS */}
      <div className="bg-white/10 p-6 rounded-3xl mb-8">
        <h2 className="text-xl mb-4">
          Notifications ({notifications.filter(n => !n.is_read).length})
        </h2>

        {notifications.map((n) => (
          <div key={n.id} className="flex justify-between p-3 bg-black/20 mb-2">
            <div>
              <p>{n.message}</p>
              <small>{n.created_at}</small>
            </div>

            {!n.is_read && (
              <button onClick={() => handleRead(n.id)}>
                Read
              </button>
            )}
          </div>
        ))}
      </div>

      {/* DOCUMENTS + COMMENTS */}
      <div className="bg-white/10 p-6 rounded-3xl">

        <h2 className="text-xl mb-4">Documents</h2>

        {documents.length === 0 && <p>No Documents</p>}

        {documents.map((doc) => (
          <div key={doc.id} className="p-4 bg-black/20 mb-4">

            <h3>{doc.file_name}</h3>

            <a
              href={`http://127.0.0.1:8000/${doc.file_path}`}
              target="_blank"
              rel="noreferrer"
              className="text-blue-300"
            >
              View
            </a>

            {/* COMMENTS */}
            <div className="mt-3">

              {(comments[doc.id] || []).map((c) => (
                <p key={c.id}>💬 {c.content}</p>
              ))}

              <input
                value={commentText[doc.id] || ""}
                onChange={(e) =>
                  setCommentText((prev) => ({
                    ...prev,
                    [doc.id]: e.target.value,
                  }))
                }
                className="text-black p-1 mt-2"
                placeholder="Add comment..."
              />

              <button
                onClick={() => handleComment(doc.id, doc.task_id)}
                className="ml-2 bg-blue-500 px-3 py-1 rounded"
              >
                Send
              </button>

            </div>

          </div>
        ))}
      </div>

    </div>
  );
}