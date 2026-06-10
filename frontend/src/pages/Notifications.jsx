import { useEffect, useState } from "react";
import { getNotifications, markNotificationRead } from "../services/api";

export default function Notifications() {
  const [notifications, setNotifications] = useState([]);
  const [error, setError] = useState("");

  const load = async () => {
    try {
      const res = await getNotifications();
      setNotifications(Array.isArray(res.data) ? res.data : []);
      setError("");
    } catch (err) {
      console.log(err);
      setError("Unable to load notifications");
    }
  };

  useEffect(() => {
    load();
  }, []);

  const markAsRead = async (id) => {
    await markNotificationRead(id);
    load();
  };

  const markAllRead = async () => {
    await Promise.all(
      notifications
        .filter((notification) => !notification.is_read)
        .map((notification) => markNotificationRead(notification.id))
    );
    load();
  };

  return (
    <div className="p-6 text-white">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Notifications</h1>

        <button
          onClick={markAllRead}
          className="px-4 py-2 bg-blue-600 rounded-lg hover:bg-blue-700"
        >
          Mark all as read
        </button>
      </div>

      {error && <p className="mb-3 text-red-300">{error}</p>}
      {notifications.length === 0 && <p className="text-gray-300">No notifications</p>}

      <div className="space-y-3">
        {notifications.map((notification) => (
          <div
            key={notification.id}
            className={`p-4 rounded-lg flex justify-between items-center ${
              notification.is_read ? "bg-gray-700" : "bg-blue-600"
            }`}
          >
            <div>
              <span>{notification.message}</span>
              <p className="text-xs opacity-80">{notification.notification_type}</p>
            </div>

            {!notification.is_read && (
              <button
                onClick={() => markAsRead(notification.id)}
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
