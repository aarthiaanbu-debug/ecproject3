export default function ErrorMessage({ message }) {
  if (!message) return null;

  return (
    <div className="mb-4 rounded-lg border border-red-400/40 bg-red-500/10 p-3 text-red-200">
      {message}
    </div>
  );
}
