export default function ToggleSwitch({ label, checked, onChange }) {
  return (
    <label className="flex items-center justify-between rounded-lg bg-white/10 p-3 text-white">
      <span>{label}</span>
      <input
        type="checkbox"
        checked={checked}
        onChange={(event) => onChange(event.target.checked)}
        className="h-5 w-5"
      />
    </label>
  );
}
