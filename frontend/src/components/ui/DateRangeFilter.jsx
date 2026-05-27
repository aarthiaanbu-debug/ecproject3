export default function DateRangeFilter({ start, end, onStart, onEnd }) {
  return (
    <>
      <input
        type="date"
        value={start}
        onChange={(event) => onStart(event.target.value)}
        className="rounded border border-white/10 bg-slate-900 p-2 text-white"
      />
      <input
        type="date"
        value={end}
        onChange={(event) => onEnd(event.target.value)}
        className="rounded border border-white/10 bg-slate-900 p-2 text-white"
      />
    </>
  );
}
