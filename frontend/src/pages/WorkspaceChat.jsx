import { useEffect, useMemo, useState } from "react";
import { Check, Edit3, RefreshCw, Send, Trash2, X } from "lucide-react";
import {
  createWorkspaceMessage,
  deleteWorkspaceMessage,
  getWorkspaceMessages,
  updateWorkspaceMessage,
} from "../api/api";

const TENANT_ID = 1;
const WORKSPACE_ID = 1;
const USER_ID = 1;

export default function WorkspaceChat() {
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState("");
  const [editingId, setEditingId] = useState(null);
  const [editingText, setEditingText] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const messageCount = useMemo(() => messages.length, [messages]);

  const loadMessages = async () => {
    setLoading(true);
    setError("");

    try {
      const res = await getWorkspaceMessages(WORKSPACE_ID);
      setMessages(res.data.items || res.data || []);
    } catch (err) {
      console.error(err);
      setError("Unable to load workspace messages");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMessages();
  }, []);

  const handleSend = async () => {
    const text = message.trim();

    if (!text) {
      return;
    }

    setSaving(true);
    setError("");

    try {
      await createWorkspaceMessage({
        tenant_id: TENANT_ID,
        workspace_id: WORKSPACE_ID,
        user_id: USER_ID,
        message: text,
      });

      setMessage("");
      await loadMessages();
    } catch (err) {
      console.error(err);
      setError("Unable to send message");
    } finally {
      setSaving(false);
    }
  };

  const startEdit = (msg) => {
    setEditingId(msg.id);
    setEditingText(msg.message);
  };

  const cancelEdit = () => {
    setEditingId(null);
    setEditingText("");
  };

  const saveEdit = async (messageId) => {
    const text = editingText.trim();

    if (!text) {
      return;
    }

    setSaving(true);
    setError("");

    try {
      await updateWorkspaceMessage(messageId, {
        tenant_id: TENANT_ID,
        user_id: USER_ID,
        message: text,
      });

      cancelEdit();
      await loadMessages();
    } catch (err) {
      console.error(err);
      setError("Unable to update message");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (messageId) => {
    const confirmed = window.confirm("Delete this message?");

    if (!confirmed) {
      return;
    }

    setSaving(true);
    setError("");

    try {
      await deleteWorkspaceMessage(messageId, {
        tenant_id: TENANT_ID,
        user_id: USER_ID,
      });

      await loadMessages();
    } catch (err) {
      console.error(err);
      setError("Unable to delete message");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 p-6 text-slate-100">
      <div className="mx-auto flex max-w-6xl flex-col gap-5">
        <div className="flex flex-col gap-3 border-b border-white/10 pb-5 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wider text-cyan-300">
              Workspace #{WORKSPACE_ID}
            </p>
            <h1 className="text-3xl font-bold">Workspace Messages</h1>
          </div>

          <div className="flex items-center gap-3">
            <span className="rounded-md border border-white/10 bg-white/5 px-3 py-2 text-sm text-slate-300">
              {messageCount} messages
            </span>
            <button
              type="button"
              onClick={loadMessages}
              className="inline-flex items-center gap-2 rounded-md bg-slate-800 px-3 py-2 text-sm font-semibold hover:bg-slate-700"
            >
              <RefreshCw size={16} />
              Refresh
            </button>
          </div>
        </div>

        {error && (
          <div className="rounded-md border border-red-400/30 bg-red-500/10 px-4 py-3 text-sm text-red-100">
            {error}
          </div>
        )}

        <div className="grid gap-5 lg:grid-cols-[1fr_340px]">
          <section className="min-h-[520px] rounded-lg border border-white/10 bg-slate-900">
            <div className="border-b border-white/10 px-5 py-4">
              <h2 className="text-lg font-semibold">Conversation</h2>
            </div>

            <div className="h-[460px] overflow-y-auto px-5 py-4">
              {loading ? (
                <div className="flex h-full items-center justify-center text-slate-400">
                  Loading messages...
                </div>
              ) : messages.length === 0 ? (
                <div className="flex h-full items-center justify-center text-slate-400">
                  No messages yet
                </div>
              ) : (
                <div className="space-y-3">
                  {messages.map((msg) => {
                    const isOwn = msg.user_id === USER_ID;
                    const isEditing = editingId === msg.id;

                    return (
                      <div
                        key={msg.id}
                        className="rounded-lg border border-white/10 bg-slate-800 px-4 py-3"
                      >
                        <div className="mb-2 flex items-center justify-between gap-3">
                          <div>
                            <p className="text-sm font-semibold text-slate-100">
                              User {msg.user_id}
                            </p>
                            <p className="text-xs text-slate-400">
                              {new Date(msg.created_at).toLocaleString()}
                            </p>
                          </div>

                          {isOwn && (
                            <div className="flex items-center gap-2">
                              {isEditing ? (
                                <>
                                  <button
                                    type="button"
                                    onClick={() => saveEdit(msg.id)}
                                    disabled={saving}
                                    className="rounded-md bg-emerald-600 p-2 hover:bg-emerald-500 disabled:opacity-60"
                                    title="Save"
                                  >
                                    <Check size={16} />
                                  </button>
                                  <button
                                    type="button"
                                    onClick={cancelEdit}
                                    className="rounded-md bg-slate-700 p-2 hover:bg-slate-600"
                                    title="Cancel"
                                  >
                                    <X size={16} />
                                  </button>
                                </>
                              ) : (
                                <>
                                  <button
                                    type="button"
                                    onClick={() => startEdit(msg)}
                                    className="rounded-md bg-slate-700 p-2 hover:bg-slate-600"
                                    title="Edit"
                                  >
                                    <Edit3 size={16} />
                                  </button>
                                  <button
                                    type="button"
                                    onClick={() => handleDelete(msg.id)}
                                    disabled={saving}
                                    className="rounded-md bg-red-600 p-2 hover:bg-red-500 disabled:opacity-60"
                                    title="Delete"
                                  >
                                    <Trash2 size={16} />
                                  </button>
                                </>
                              )}
                            </div>
                          )}
                        </div>

                        {isEditing ? (
                          <textarea
                            value={editingText}
                            onChange={(event) => setEditingText(event.target.value)}
                            className="min-h-24 w-full resize-none rounded-md border border-cyan-400/40 bg-slate-950 p-3 text-sm text-white outline-none"
                          />
                        ) : (
                          <p className="whitespace-pre-wrap text-sm leading-6 text-slate-200">
                            {msg.message}
                          </p>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </section>

          <aside className="rounded-lg border border-white/10 bg-slate-900 p-5">
            <h2 className="text-lg font-semibold">New Message</h2>

            <textarea
              value={message}
              onChange={(event) => setMessage(event.target.value)}
              placeholder="Write a workspace update..."
              className="mt-4 min-h-40 w-full resize-none rounded-md border border-white/10 bg-slate-950 p-3 text-sm text-white outline-none focus:border-cyan-400"
            />

            <button
              type="button"
              onClick={handleSend}
              disabled={saving || !message.trim()}
              className="mt-4 inline-flex w-full items-center justify-center gap-2 rounded-md bg-cyan-600 px-4 py-3 text-sm font-bold text-white hover:bg-cyan-500 disabled:cursor-not-allowed disabled:opacity-60"
            >
              <Send size={17} />
              Send Message
            </button>
          </aside>
        </div>
      </div>
    </div>
  );
}
