import { useEffect, useState } from "react";
import {
  createChannelMessage,
  getChannelMessages,
} from "../api/api";

export default function ChannelChat() {
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState("");

  const channelId = 1;

  const loadMessages = async () => {
    const res = await getChannelMessages(channelId);
    setMessages(res.data.items || res.data);
  };

  useEffect(() => {
    loadMessages();
  }, []);

  const handleSend = async () => {
    await createChannelMessage({
      tenant_id: 1,
      workspace_id: 1,
      channel_id: channelId,
      sender_id: 1,
      content: message,
    });

    setMessage("");
    loadMessages();
  };

  return (
    <div className="p-6 text-white">
      <h1 className="text-3xl font-bold mb-5">
        Channel Chat
      </h1>

      <div className="bg-white text-black p-4 rounded h-96 overflow-auto">
        {messages.map((msg) => (
          <div key={msg.id}>{msg.content}</div>
        ))}
      </div>

      <div className="flex gap-2 mt-4">
        <input
          className="flex-1 p-3 rounded text-black"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />

        <button
          onClick={handleSend}
          className="bg-blue-600 px-4 py-2 rounded"
        >
          Send
        </button>
      </div>
    </div>
  );
}
