import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { getStripeSession } from "../services/api";

export default function Success() {
  const [searchParams] = useSearchParams();
  const [session, setSession] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const sessionId = searchParams.get("session_id");

    if (!sessionId) {
      return;
    }

    getStripeSession(sessionId)
      .then((res) => setSession(res.data))
      .catch((err) =>
        setError(err.response?.data?.detail || "Unable to verify payment")
      );
  }, [searchParams]);

  return (
    <div style={{ padding: "50px", color: "green" }}>
      <h1>Payment Successful</h1>
      <p>Your subscription is activated.</p>

      {session && (
        <div style={{ marginTop: "16px", color: "white" }}>
          <p>Plan: {session.plan?.toUpperCase() || "N/A"}</p>
          <p>Payment status: {session.payment_status}</p>
        </div>
      )}

      {error && <p style={{ color: "#fca5a5" }}>{error}</p>}
    </div>
  );
}
