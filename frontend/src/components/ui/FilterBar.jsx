export default function FilterBar({ children }) {
  return (
    <div className="mb-5 grid gap-3 rounded-lg border border-white/10 bg-white/10 p-4 md:grid-cols-3">
      {children}
    </div>
  );
}
