import { Bell } from "lucide-react";

export default function NotificationBell({ notifications = [] }) {

  const unread = notifications.filter(n => !n.is_read).length;

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