import { useState } from "react";
import API from "../services/api";
import { useSearchParams } from "react-router-dom";

export default function ResetPassword() {

  const [searchParams] = useSearchParams();

  const token = searchParams.get("token");

  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {

      const res = await API.post(
        "/auth/reset-password",
        null,
        {
          params: {
            token,
            new_password: password,
          },
        }
      );

      alert(res.data.message);

    } catch (err) {

      console.log(err.response?.data);

      alert(
        err.response?.data?.detail ||
        err.response?.data?.message ||
        "Error"
      );
    }
  };

  return (
    <div className="flex justify-center items-center h-screen">

      <form
        onSubmit={handleSubmit}
        className="bg-slate-800 p-8 rounded w-96"
      >

        <h1 className="text-3xl mb-6 text-white">
          Reset Password
        </h1>

        <input
          type="password"
          placeholder="New Password"
          className="w-full p-3 mb-4 rounded"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          className="bg-green-500 w-full p-3 rounded text-white"
        >
          Reset Password
        </button>

      </form>

    </div>
  );
}