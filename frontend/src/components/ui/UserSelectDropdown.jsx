export default function UserSelectDropdown({ value, onChange }) {
  const users = [
    { id: 1, name: "Aarthi" },
    { id: 2, name: "Manager" },
    { id: 3, name: "Admin" },
  ];

  return (
    <select
      value={value}
      onChange={(event) => onChange(event.target.value)}
      className="rounded border border-white/10 bg-slate-900 p-2 text-white"
    >
      <option value="">Select user</option>
      {users.map((user) => (
        <option key={user.id} value={user.id}>
          {user.name}
        </option>
      ))}
    </select>
  );
}
