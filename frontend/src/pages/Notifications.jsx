import { useState } from "react";

export default function Notifications() {
  const [notifications, setNotifications] = useState([
    { id: 1, message: "New task assigned to you", read: false },
    { id: 2, message: "Your report was approved", read: false },
    { id: 3, message: "New comment on Kanban board", read: true },
  ]);

  const markAsRead = (id) => {
    setNotifications((prev) =>
      prev.map((n) =>
        n.id === id ? { ...n, read: true } : n
      )
    );
  };

  const markAllRead = () => {
    setNotifications((prev) =>
      prev.map((n) => ({ ...n, read: true }))
    );
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Notifications</h1>

        <button
          onClick={markAllRead}
          className="px-4 py-2 bg-blue-600 rounded-lg hover:bg-blue-700"
        >
          Mark all as read
        </button>
      </div>

      <div className="space-y-3">
        {notifications.map((n) => (
          <div
            key={n.id}
            className={`p-4 rounded-lg flex justify-between items-center ${
              n.read ? "bg-gray-700" : "bg-blue-600"
            }`}
          >
            <span>{n.message}</span>

            {!n.read && (
              <button
                onClick={() => markAsRead(n.id)}
                className="text-sm bg-white text-black px-3 py-1 rounded"
              >
                Mark read
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}