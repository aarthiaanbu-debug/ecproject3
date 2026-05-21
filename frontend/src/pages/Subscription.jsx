import { useState } from "react";
import { createStripeSession } from "../services/api";

export default function Subscription() {
  const [loading, setLoading] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState("");
  const [checkoutUrl, setCheckoutUrl] = useState("");
  const [error, setError] = useState("");

  const plans = [
    {
      name: "pro",
      price: "Rs. 499",
      features: ["Tasks Access", "Basic Analytics", "Email Support"],
    },
    {
      name: "premium",
      price: "Rs. 999",
      features: ["Everything in Pro", "AI Insights", "Priority Support"],
    },
  ];

  const handleSubscribe = async (plan) => {
    try {
      setLoading(true);
      setSelectedPlan(plan);
      setCheckoutUrl("");
      setError("");

      const res = await createStripeSession(plan);
      const url = res.data.url;

      if (url) {
        setCheckoutUrl(url);
        window.location.href = url;
      } else {
        setError("No checkout URL received");
      }
    } catch (err) {
      console.log(err);
      const message =
        err.response?.data?.detail || "Payment failed. Please try again.";
      setError(message);
      alert(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "30px", color: "white" }}>
      <h1>Choose Your Plan</h1>

      {error && (
        <p style={{ color: "#fca5a5", marginTop: "12px" }}>{error}</p>
      )}

      {checkoutUrl && (
        <p style={{ marginTop: "12px" }}>
          Checkout URL:{" "}
          <a href={checkoutUrl} style={{ color: "#93c5fd" }}>
            {checkoutUrl}
          </a>
        </p>
      )}

      <div style={{ display: "flex", gap: "20px", marginTop: "20px" }}>
        {plans.map((plan) => (
          <div
            key={plan.name}
            style={{
              border: "1px solid gray",
              padding: "20px",
              borderRadius: "10px",
              width: "200px",
            }}
          >
            <h2>{plan.name.toUpperCase()}</h2>
            <h3>{plan.price}</h3>

            <ul>
              {plan.features.map((feature) => (
                <li key={feature}>{feature}</li>
              ))}
            </ul>

            <button
              disabled={loading}
              onClick={() => handleSubscribe(plan.name)}
              style={{
                marginTop: "10px",
                padding: "10px",
                width: "100%",
                background: "blue",
                color: "white",
                border: "none",
                cursor: "pointer",
              }}
            >
              {loading && selectedPlan === plan.name
                ? "Processing..."
                : "Subscribe"}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
