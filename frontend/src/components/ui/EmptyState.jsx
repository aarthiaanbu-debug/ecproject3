export default function EmptyState({ message = "No records found" }) {
  return (
    <div className="rounded-lg border border-white/10 bg-white/10 p-5 text-slate-300">
      {message}
    </div>
  );
}
