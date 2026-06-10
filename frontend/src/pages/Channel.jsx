import { useEffect, useState } from "react";
import {
  createChannel,
  getWorkspaceChannels,
  joinChannel,
  leaveChannel,
  archiveChannel,
  restoreChannel,
} from "../api/api";

export default function Channel() {
  const [channels, setChannels] = useState([]);

  const [form, setForm] = useState({
    tenant_id: 1,
    workspace_id: 1,
    name: "",
    description: "",
    channel_type: "PUBLIC",
    created_by: 1,
  });

  useEffect(() => {
    loadChannels();
  }, []);

  const loadChannels = async () => {
    try {
      const res = await getWorkspaceChannels(1);

      if (Array.isArray(res.data)) {
        setChannels(res.data);
      } else {
        setChannels([]);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();

    try {
      await createChannel(form);

      alert("Channel Created Successfully");

      setForm({
        tenant_id: 1,
        workspace_id: 1,
        name: "",
        description: "",
        channel_type: "PUBLIC",
        created_by: 1,
      });

      loadChannels();
    } catch (err) {
      console.error(err);
      alert("Failed to create channel");
    }
  };

  const handleJoin = async (channelId) => {
    try {
      await joinChannel(channelId, 1);
      alert("Joined Channel");
      loadChannels();
    } catch (err) {
      console.error(err);
      alert("Unable to join");
    }
  };

  const handleLeave = async (channelId) => {
    try {
      await leaveChannel(channelId, 1);
      alert("Left Channel");
      loadChannels();
    } catch (err) {
      console.error(err);
      alert("Unable to leave");
    }
  };

  const handleArchive = async (id) => {
    try {
      await archiveChannel(id);
      alert("Channel Archived");
      loadChannels();
    } catch (err) {
      console.error(err);
    }
  };

  const handleRestore = async (id) => {
    try {
      await restoreChannel(id);
      alert("Channel Restored");
      loadChannels();
    } catch (err) {
      console.error(err);
    }
  };

  const handleEdit = (channel) => {
    setForm({
      tenant_id: channel.tenant_id,
      workspace_id: channel.workspace_id,
      name: channel.name,
      description: channel.description || "",
      channel_type: channel.channel_type,
      created_by: channel.created_by,
    });

    alert("Channel data loaded into form");
  };

  return (
    <div className="p-8 text-white">
      <h1 className="text-4xl font-bold mb-2">Channels</h1>

      <p className="text-gray-400 mb-8">
        Browse and manage channels
      </p>

      <div className="bg-white rounded-2xl p-6 shadow-lg">
        <form onSubmit={handleCreate}>
          <input
            type="text"
            placeholder="Channel Name"
            value={form.name}
            onChange={(e) =>
              setForm({
                ...form,
                name: e.target.value,
              })
            }
            className="w-full border p-3 rounded mb-4 text-black"
            required
          />

          <textarea
            placeholder="Description"
            value={form.description}
            onChange={(e) =>
              setForm({
                ...form,
                description: e.target.value,
              })
            }
            className="w-full border p-3 rounded mb-4 text-black"
          />

          <select
            value={form.channel_type}
            onChange={(e) =>
              setForm({
                ...form,
                channel_type: e.target.value,
              })
            }
            className="w-full border p-3 rounded mb-4 text-black"
          >
            <option value="PUBLIC">PUBLIC</option>
            <option value="PRIVATE">PRIVATE</option>
            <option value="ANNOUNCEMENT">ANNOUNCEMENT</option>
            <option value="PROJECT">PROJECT</option>
          </select>

          <button
            type="submit"
            className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-lg"
          >
            Create Channel
          </button>
        </form>
      </div>

      <div className="grid md:grid-cols-3 gap-6 mt-8">
        {channels.map((channel) => (
          <div
            key={channel.id}
            className="bg-white text-black rounded-2xl shadow-lg p-5"
          >
            <div className="flex justify-between items-center">
              <h2 className="font-bold text-lg">
                #{channel.name}
              </h2>

              <span className="text-xs bg-gray-200 px-2 py-1 rounded">
                {channel.channel_type}
              </span>
            </div>

            <p className="text-gray-600 mt-3">
              {channel.description}
            </p>

            <div className="flex flex-wrap gap-2 mt-5">
              <button
                onClick={() => handleJoin(channel.id)}
                className="bg-green-500 hover:bg-green-600 text-white px-3 py-2 rounded"
              >
                Join
              </button>

              <button
                onClick={() => handleLeave(channel.id)}
                className="bg-red-500 hover:bg-red-600 text-white px-3 py-2 rounded"
              >
                Leave
              </button>

              <button
                onClick={() => handleEdit(channel)}
                className="bg-yellow-500 hover:bg-yellow-600 text-white px-3 py-2 rounded"
              >
                Edit
              </button>

              <button
                onClick={() => handleArchive(channel.id)}
                className="bg-orange-500 hover:bg-orange-600 text-white px-3 py-2 rounded"
              >
                Archive
              </button>

              <button
                onClick={() => handleRestore(channel.id)}
                className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-2 rounded"
              >
                Restore
              </button>
            </div>
          </div>
        ))}
      </div>

      {channels.length === 0 && (
        <div className="text-center text-gray-400 mt-10">
          No channels found
        </div>
      )}
    </div>
  );
}