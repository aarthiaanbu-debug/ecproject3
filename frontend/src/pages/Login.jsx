import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { loginUser } from "../services/api";

export default function Login() {

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await loginUser({ email, password });

      localStorage.setItem("token", res.data.access_token);
      localStorage.setItem("refresh_token", res.data.refresh_token);
      localStorage.setItem(
        "role",
        String(res.data.role || "employee").trim().toLowerCase()
      );

      alert("Login Success");
      navigate("/dashboard");

    } catch (err) {
      alert(err.response?.data?.detail || "Login Failed");
    }
  };

  return (
    <div className="h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 to-slate-950">

      <div className="w-[400px] p-8 bg-white/10 backdrop-blur rounded-2xl border border-white/10">

        <h1 className="text-3xl font-bold mb-2">Welcome Back</h1>
        <p className="text-gray-400 mb-6">Login to continue</p>

        <form onSubmit={handleSubmit}>

          <input
            className="w-full p-3 mb-3 bg-black/20 rounded"
            placeholder="Email"
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            className="w-full p-3 mb-3 bg-black/20 rounded"
            type="password"
            placeholder="Password"
            onChange={(e) => setPassword(e.target.value)}
          />

          <button className="w-full bg-cyan-500 p-3 rounded font-bold">
            Login
          </button>

        </form>

        <p className="mt-4 text-center text-sm">
          Don't have account?{" "}
          <span className="text-cyan-400 cursor-pointer" onClick={() => navigate("/register")}>
            Register
          </span>
        </p>

      </div>
    </div>
  );
}
