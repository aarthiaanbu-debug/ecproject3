import { useEffect, useState } from "react";
import { Bell } from "lucide-react";
import { getNotifications } from "../services/api";

export default function NotificationBell() {
  const [unread, setUnread] = useState(0);

  useEffect(() => {
    getNotifications()
      .then((res) => {
        const notifications = Array.isArray(res.data) ? res.data : [];
        setUnread(notifications.filter((item) => !item.is_read).length);
      })
      .catch(() => setUnread(0));
  }, []);

  return (
    <div className="relative">
      <Bell className="text-white" />

      {unread > 0 && (
        <span className="absolute -top-2 -right-2 bg-red-500 text-xs px-2 rounded-full">
          {unread}
        </span>
      )}
    </div>
  );
}
