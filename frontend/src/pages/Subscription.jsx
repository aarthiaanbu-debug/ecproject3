import { useState } from "react";
import { createStripeSession } from "../services/api";

export default function Subscription() {
  const [loading, setLoading] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState("");

  const plans = [
    {
      name: "pro",
      price: "₹499",
      features: ["Tasks Access", "Basic Analytics", "Email Support"],
    },
    {
      name: "premium",
      price: "₹999",
      features: ["Everything in Pro", "AI Insights", "Priority Support"],
    },
  ];

  const handleSubscribe = async (plan) => {
    try {
      setLoading(true);
      setSelectedPlan(plan);

      const res = await createStripeSession({ plan });

      // backend returns: { url: "https://checkout.stripe.com/..." }
      const checkoutUrl = res.data.url;

      if (checkoutUrl) {
        window.location.href = checkoutUrl; // 🔥 redirect to Stripe
      } else {
        alert("No checkout URL received");
      }
    } catch (err) {
      console.log(err);
      alert("Payment failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "30px", color: "white" }}>
      <h1>Choose Your Plan</h1>

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
              {plan.features.map((f, i) => (
                <li key={i}>{f}</li>
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