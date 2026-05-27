import StatusBadge from "./StatusBadge";

export default function SLABadge({ status, breached }) {
  if (breached) {
    return <StatusBadge value="breached" />;
  }

  return <StatusBadge value={status || "not started"} />;
}
