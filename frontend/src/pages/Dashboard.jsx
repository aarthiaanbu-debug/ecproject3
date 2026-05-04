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

      // ANALYTICS
      const analyticsRes = await getAnalytics();
      setData(analyticsRes.data);

      // NOTIFICATIONS
      const notificationRes = await getNotifications();
      setNotifications(notificationRes.data || []);

      // DOCUMENTS
      const documentRes = await getDocuments();

      console.log("DOCUMENT RESPONSE:", documentRes.data);

      // IMPORTANT FIX
      const docs =
        Array.isArray(documentRes.data)
          ? documentRes.data
          : documentRes.data.documents || [];

      setDocuments(docs);

      // COMMENTS
      const tempComments = {};

      for (const doc of docs) {

        try {

          // task_id இல்லனா skip
          if (!doc.task_id) {
            tempComments[doc.id] = [];
            continue;
          }

          const res = await getComments(doc.task_id);

          tempComments[doc.id] = res.data || [];

        } catch (err) {

          console.log(err);

          tempComments[doc.id] = [];
        }
      }

      console.log("COMMENTS:", tempComments);

      setComments(tempComments);

    } catch (err) {

      console.log(err);

    }
  };

  // =========================
  // READ NOTIFICATION
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
  // ADD COMMENT
  // =========================

  const handleComment = async (docId, taskId) => {

    if (!commentText[docId]) return;

    try {

      await addComment(
        taskId,
        commentText[docId]
      );

      setCommentText({
        ...commentText,
        [docId]: "",
      });

      loadDashboard();

    } catch (err) {

      console.log(err);

    }
  };

  // =========================
  // LOADING
  // =========================

  if (!data) {
    return (
      <div className="text-white text-xl">
        Loading...
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

        <h1 className="text-4xl font-bold">
          📊 Dashboard Analytics
        </h1>

        <p className="text-gray-400 mt-2">
          Enterprise Workflow Monitoring
        </p>

      </div>

      {/* CARDS */}

      <div className="grid md:grid-cols-4 gap-6 mb-8">

        <div className="bg-gradient-to-r from-purple-500 to-indigo-600 p-6 rounded-3xl shadow-xl">

          <h2 className="text-lg">
            Total Tasks
          </h2>

          <p className="text-4xl font-bold mt-4">
            {total}
          </p>

        </div>

        <div className="bg-gradient-to-r from-blue-500 to-cyan-500 p-6 rounded-3xl shadow-xl">

          <h2 className="text-lg">
            Todo
          </h2>

          <p className="text-4xl font-bold mt-4">
            {todo}
          </p>

        </div>

        <div className="bg-gradient-to-r from-yellow-500 to-orange-500 p-6 rounded-3xl shadow-xl">

          <h2 className="text-lg">
            In Progress
          </h2>

          <p className="text-4xl font-bold mt-4">
            {inprogress}
          </p>

        </div>

        <div className="bg-gradient-to-r from-green-500 to-emerald-500 p-6 rounded-3xl shadow-xl">

          <h2 className="text-lg">
            Done
          </h2>

          <p className="text-4xl font-bold mt-4">
            {done}
          </p>

        </div>

      </div>

      {/* TASK DISTRIBUTION */}

      <div className="bg-white/10 p-6 rounded-3xl mb-8 border border-white/10">

        <h2 className="text-2xl font-bold mb-6">
          📈 Task Distribution
        </h2>

        <div className="space-y-5">

          <div>

            <div className="flex justify-between mb-1">

              <span>Todo</span>

              <span>{percent(todo)}%</span>

            </div>

            <div className="w-full bg-gray-700 h-3 rounded-full">

              <div
                className="bg-blue-400 h-3 rounded-full"
                style={{
                  width: `${percent(todo)}%`
                }}
              ></div>

            </div>

          </div>

          <div>

            <div className="flex justify-between mb-1">

              <span>In Progress</span>

              <span>{percent(inprogress)}%</span>

            </div>

            <div className="w-full bg-gray-700 h-3 rounded-full">

              <div
                className="bg-yellow-400 h-3 rounded-full"
                style={{
                  width: `${percent(inprogress)}%`
                }}
              ></div>

            </div>

          </div>

          <div>

            <div className="flex justify-between mb-1">

              <span>Done</span>

              <span>{percent(done)}%</span>

            </div>

            <div className="w-full bg-gray-700 h-3 rounded-full">

              <div
                className="bg-green-400 h-3 rounded-full"
                style={{
                  width: `${percent(done)}%`
                }}
              ></div>

            </div>

          </div>

        </div>

      </div>

      {/* PERFORMANCE */}

      <div className="bg-white/10 p-6 rounded-3xl border border-white/10 mb-8">

        <h2 className="text-2xl font-bold mb-5">
          🚀 Performance Insights
        </h2>

        <ul className="space-y-3 text-lg">

          {inprogress > 0 && (
            <li className="text-yellow-400">
              ⚠️ Tasks are in progress — Keep going!
            </li>
          )}

          {todo > done && (
            <li className="text-red-400">
              🔴 Many tasks pending — Need attention!
            </li>
          )}

          {done > 0 && done < total && (
            <li className="text-green-400">
              ✅ Tasks are getting completed successfully
            </li>
          )}

        </ul>

        <div className="grid md:grid-cols-2 gap-4 mt-6">

          {avg_completion_time > 0 && (
            <div className="bg-white/5 p-4 rounded-xl">
              ⏱ Avg Completion Time:
              <span className="text-purple-300 font-bold ml-2">
                {avg_completion_time}
              </span>
            </div>
          )}

          {overdue > 0 && (
            <div className="bg-white/5 p-4 rounded-xl">
              ⏰ Overdue Tasks:
              <span className="text-red-400 font-bold ml-2">
                {overdue}
              </span>
            </div>
          )}

          {due_today > 0 && (
            <div className="bg-white/5 p-4 rounded-xl">
              📅 Tasks Due Today:
              <span className="text-yellow-300 font-bold ml-2">
                {due_today}
              </span>
            </div>
          )}

          <div className="bg-white/5 p-4 rounded-xl">
            🏆 Top Performer:
            <span className="text-green-300 font-bold ml-2">
              {top_performer}
            </span>
          </div>

        </div>

      </div>

      {/* NOTIFICATIONS */}

      <div className="bg-white/10 p-6 rounded-3xl border border-white/10 mb-8">

        <div className="flex justify-between items-center mb-5">

          <h2 className="text-2xl font-bold">
            🔔 Notifications
          </h2>

          <span className="bg-red-500 px-3 py-1 rounded-full text-sm">
            {
              notifications.filter((n) => !n.is_read).length
            }
          </span>

        </div>

        <div className="space-y-4">

          {notifications.map((note) => (

            <div
              key={note.id}
              className="bg-white/5 p-4 rounded-2xl flex justify-between items-center"
            >

              <div>

                <p className="font-semibold">
                  {note.message}
                </p>

                <p className="text-sm text-gray-400">
                  {note.created_at}
                </p>

              </div>

              {!note.is_read && (

                <button
                  onClick={() => handleRead(note.id)}
                  className="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded-xl"
                >
                  Read
                </button>

              )}

            </div>

          ))}

        </div>

      </div>

      {/* DOCUMENTS */}

      <div className="bg-white/10 p-6 rounded-3xl border border-white/10">

        <h2 className="text-2xl font-bold mb-6">
          📂 Documents
        </h2>

        {documents.length === 0 && (

          <div className="bg-black/20 p-5 rounded-2xl text-center text-gray-400">
            No Documents Found
          </div>

        )}

        <div className="space-y-6">

          {documents.map((doc) => (

            <div
              key={doc.id}
              className="bg-white/5 p-5 rounded-2xl border border-white/10"
            >

              <div className="flex justify-between items-center mb-5">

                <div>

                  <h3 className="text-xl font-bold">
                    {doc.file_name}
                  </h3>

                  <p className="text-gray-400 text-sm mt-1">
                    Version: {doc.version}
                  </p>

                  <p className="text-gray-500 text-xs mt-1">
                    {doc.created_at}
                  </p>

                </div>

                <a
                  href={`http://127.0.0.1:8000/${doc.file_path}`}
                  target="_blank"
                  rel="noreferrer"
                  className="bg-green-500 hover:bg-green-600 px-5 py-2 rounded-xl"
                >
                  View
                </a>

              </div>

              {/* COMMENTS */}

              <div>

                <h4 className="font-bold mb-3">
                  💬 Comments
                </h4>

                <div className="space-y-2 mb-4">

                  {(comments[doc.id] || []).length === 0 && (

                    <div className="text-gray-400 text-sm">
                      No comments yet
                    </div>

                  )}

                  {(comments[doc.id] || []).map((c) => (

                    <div
                      key={c.id}
                      className="bg-black/20 p-3 rounded-xl"
                    >
                      {c.content}
                    </div>

                  ))}

                </div>

                {/* ADD COMMENT */}

                <div className="flex gap-3">

                  <input
                    type="text"
                    placeholder="Add comment..."
                    value={commentText[doc.id] || ""}
                    onChange={(e) =>
                      setCommentText({
                        ...commentText,
                        [doc.id]: e.target.value,
                      })
                    }
                    className="flex-1 bg-black/20 border border-white/10 p-3 rounded-xl outline-none"
                  />

                  <button
                    onClick={() =>
                      handleComment(doc.id, doc.task_id)
                    }
                    className="bg-cyan-500 hover:bg-cyan-600 px-5 rounded-xl"
                  >
                    Send
                  </button>

                </div>

              </div>

            </div>

          ))}

        </div>

      </div>

    </div>
  );
}