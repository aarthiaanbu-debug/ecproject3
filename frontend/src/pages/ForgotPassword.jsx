import { useState } from "react";

import {
  forgotPassword
} from "../services/api";

export default function ForgotPassword() {

  const [email, setEmail] =
    useState("");

  const handleForgot = async () => {

    try {

      const res =
        await forgotPassword(email);

      alert(res.data.message);

    } catch (err) {

      alert("Error");
    }
  };

  return (

    <div className="flex justify-center items-center h-screen">

      <div className="bg-slate-800 p-8 rounded w-96">

        <h1 className="text-2xl mb-5">
          Forgot Password
        </h1>

        <input
          type="email"
          placeholder="Enter email"
          className="w-full p-2 mb-4 text-black"
          onChange={(e) =>
            setEmail(e.target.value)
          }
        />

        <button
          onClick={handleForgot}
          className="bg-blue-500 px-4 py-2 w-full"
        >
          Send Reset Link
        </button>

      </div>

    </div>
  );
}