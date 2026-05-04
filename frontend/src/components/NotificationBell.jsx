// frontend/src/components/NotificationBell.jsx

import { useEffect, useState } from "react";
import { getNotifications } from "../services/api";

export default function NotificationBell() {

  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    loadNotifications();
  }, []);

  const loadNotifications = async () => {

    try {

      const res = await getNotifications();

      setNotifications(res.data || []);

    } catch (err) {

      console.log(err);

    }
  };

  const unreadCount = notifications.filter(
    (n) => !n.is_read
  ).length;

  return (

    <div className="relative cursor-pointer">

      <div className="text-2xl hover:scale-110 transition">
        🔔
      </div>

      {unreadCount > 0 && (

        <span
          className="
            absolute
            -top-2
            -right-2
            bg-red-500
            text-white
            text-xs
            min-w-[20px]
            h-5
            px-1
            flex
            items-center
            justify-center
            rounded-full
            font-bold
          "
        >
          {unreadCount}
        </span>

      )}

    </div>
  );
}