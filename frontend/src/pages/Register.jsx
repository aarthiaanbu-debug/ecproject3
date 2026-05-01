import { useState } from "react";
import { registerUser } from "../services/api";
import { useNavigate } from "react-router-dom";

export default function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    role: "user"
  });

  const handleSubmit = async () => {
    await registerUser(form);
    navigate("/");
  };

  return (
    <div className="h-screen flex items-center justify-center bg-gradient-to-r from-green-400 to-blue-500">
      <div className="bg-white p-8 rounded-xl shadow-xl w-80">
        <h2 className="text-xl font-bold mb-4">Register</h2>

        <input placeholder="Name" className="border p-2 w-full mb-2"
          onChange={(e) => setForm({ ...form, name: e.target.value })} />

        <input placeholder="Email" className="border p-2 w-full mb-2"
          onChange={(e) => setForm({ ...form, email: e.target.value })} />

        <input type="password" placeholder="Password" className="border p-2 w-full mb-2"
          onChange={(e) => setForm({ ...form, password: e.target.value })} />

        <select className="border p-2 w-full mb-3"
          onChange={(e) => setForm({ ...form, role: e.target.value })}>
          <option value="user">User</option>
          <option value="manager">Manager</option>
          <option value="admin">Admin</option>
        </select>

        <button
          onClick={handleSubmit}
          className="bg-green-500 text-white w-full py-2 rounded"
        >
          Register
        </button>
      </div>
    </div>
  );
}