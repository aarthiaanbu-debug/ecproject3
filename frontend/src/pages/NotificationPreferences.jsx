import { useEffect, useState } from "react";
import ErrorMessage from "../components/ui/ErrorMessage";
import PageHeader from "../components/ui/PageHeader";
import ToggleSwitch from "../components/ui/ToggleSwitch";
import {
  getNotificationPreferences,
  updateNotificationPreferences,
} from "../services/api";

export default function NotificationPreferences() {
  const [prefs, setPrefs] = useState(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    getNotificationPreferences()
      .then((res) => setPrefs(res.data))
      .catch(() => setError("Unable to load preferences"));
  }, []);

  const setValue = (key, value) => setPrefs({ ...prefs, [key]: value });

  const save = async () => {
    try {
      await updateNotificationPreferences(prefs);
      setMessage("Preferences saved");
      setError("");
    } catch {
      setError("Unable to save preferences");
    }
  };

  if (!prefs) return <div className="p-6 text-white">Loading...</div>;

  return (
    <div className="p-6">
      <PageHeader title="Notification Preferences" subtitle="Control workflow notification channels" />
      <ErrorMessage message={error} />
      {message && <div className="mb-4 rounded bg-green-500/20 p-3 text-green-200">{message}</div>}
      <div className="grid gap-3 rounded-lg bg-white/10 p-5 md:grid-cols-2">
        <ToggleSwitch label="In-app Notifications" checked={prefs.in_app_enabled} onChange={(value) => setValue("in_app_enabled", value)} />
        <ToggleSwitch label="Email Notifications" checked={prefs.email_enabled} onChange={(value) => setValue("email_enabled", value)} />
        <ToggleSwitch label="Task Notifications" checked={prefs.task_notifications} onChange={(value) => setValue("task_notifications", value)} />
        <ToggleSwitch label="Approval Notifications" checked={prefs.approval_notifications} onChange={(value) => setValue("approval_notifications", value)} />
        <ToggleSwitch label="Escalation Notifications" checked={prefs.escalation_notifications} onChange={(value) => setValue("escalation_notifications", value)} />
        <ToggleSwitch label="Document Notifications" checked={prefs.document_notifications} onChange={(value) => setValue("document_notifications", value)} />
      </div>
      <button onClick={save} className="mt-5 rounded bg-blue-600 px-5 py-2 text-white">Save</button>
    </div>
  );
}
