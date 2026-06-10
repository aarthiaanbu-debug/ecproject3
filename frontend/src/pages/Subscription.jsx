import { useMemo, useState } from "react";
import { createStripeSession } from "../services/api";

const plans = [
  {
    id: "pro",
    title: "Pro",
    price: "Rs. 499",
    period: "one time",
    description: "Best for employees and small teams starting workflow tracking.",
    features: ["Task management", "Kanban workflow", "Basic analytics", "Email support"],
    highlight: false,
  },
  {
    id: "premium",
    title: "Premium",
    price: "Rs. 999",
    period: "one time",
    description: "For managers who need approvals, SLA visibility, and reports.",
    features: ["Everything in Pro", "Approval workflow", "SLA dashboard", "Priority support"],
    highlight: true,
  },
  {
    id: "gold",
    title: "Gold",
    price: "Rs. 1,999",
    period: "one time",
    description: "Enterprise-ready access for admin governance and audit review.",
    features: ["Everything in Premium", "Audit logs", "Tenant usage", "Admin controls"],
    highlight: false,
  },
];

export default function Subscription() {
  const storedName =
    localStorage.getItem("name") ||
    localStorage.getItem("username") ||
    localStorage.getItem("email") ||
    "";

  const [customerName, setCustomerName] = useState(storedName);
  const [loadingPlan, setLoadingPlan] = useState("");
  const [selectedPlan, setSelectedPlan] = useState("");
  const [checkoutUrl, setCheckoutUrl] = useState("");
  const [error, setError] = useState("");

  const selectedPlanTitle = useMemo(() => {
    return plans.find((plan) => plan.id === selectedPlan)?.title || "";
  }, [selectedPlan]);

  const handleSubscribe = async (planId) => {
    const cleanName = customerName.trim();

    if (!cleanName) {
      setError("Please enter customer name before checkout.");
      return;
    }

    try {
      setError("");
      setCheckoutUrl("");
      setSelectedPlan(planId);
      setLoadingPlan(planId);

      const res = await createStripeSession({
        plan: planId,
        customer_name: cleanName,
      });

      const url = res.data?.url;
      if (!url) {
        setError("No checkout URL received from backend.");
        return;
      }

      setCheckoutUrl(url);
      window.location.href = url;
    } catch (err) {
      const message =
        err.response?.data?.detail || "Payment checkout failed. Please try again.";
      setError(message);
    } finally {
      setLoadingPlan("");
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 px-6 py-8 text-white">
      <div className="mx-auto max-w-7xl">
        <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wide text-blue-300">
              EC App Billing
            </p>
            <h1 className="mt-2 text-4xl font-bold">Subscription Plans</h1>
            <p className="mt-3 max-w-2xl text-slate-300">
              Select a plan for the customer and continue to Stripe secure checkout.
            </p>
          </div>

          <div className="w-full rounded-lg border border-slate-700 bg-slate-900 p-4 shadow-lg md:w-96">
            <label className="block text-sm font-semibold text-slate-200">
              Customer Name
            </label>
            <input
              value={customerName}
              onChange={(event) => setCustomerName(event.target.value)}
              placeholder="Enter customer name"
              className="mt-2 w-full rounded-md border border-slate-600 bg-slate-800 px-4 py-3 text-white outline-none transition focus:border-blue-400"
            />
            {selectedPlanTitle && (
              <p className="mt-3 text-sm text-slate-300">
                Processing plan:{" "}
                <span className="font-semibold text-blue-300">{selectedPlanTitle}</span>
              </p>
            )}
          </div>
        </div>

        {error && (
          <div className="mb-6 rounded-md border border-red-500/40 bg-red-500/10 px-4 py-3 text-red-200">
            {error}
          </div>
        )}

        {checkoutUrl && (
          <div className="mb-6 rounded-md border border-blue-500/40 bg-blue-500/10 px-4 py-3 text-blue-100">
            Checkout URL ready:{" "}
            <a className="font-semibold underline" href={checkoutUrl}>
              Open Stripe Checkout
            </a>
          </div>
        )}

        <div className="grid gap-5 lg:grid-cols-3">
          {plans.map((plan) => {
            const isLoading = loadingPlan === plan.id;

            return (
              <section
                key={plan.id}
                className={`rounded-lg border p-6 shadow-xl transition ${
                  plan.highlight
                    ? "border-blue-400 bg-slate-900"
                    : "border-slate-700 bg-slate-900/80"
                }`}
              >
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <h2 className="text-2xl font-bold">{plan.title}</h2>
                    <p className="mt-2 min-h-12 text-sm text-slate-300">
                      {plan.description}
                    </p>
                  </div>
                  {plan.highlight && (
                    <span className="rounded-full bg-blue-500 px-3 py-1 text-xs font-bold text-white">
                      Popular
                    </span>
                  )}
                </div>

                <div className="mt-6">
                  <span className="text-4xl font-bold">{plan.price}</span>
                  <span className="ml-2 text-sm text-slate-400">{plan.period}</span>
                </div>

                <ul className="mt-6 space-y-3 text-sm text-slate-200">
                  {plan.features.map((feature) => (
                    <li key={feature} className="flex gap-3">
                      <span className="mt-1 h-2 w-2 rounded-full bg-green-400" />
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>

                <button
                  type="button"
                  disabled={Boolean(loadingPlan)}
                  onClick={() => handleSubscribe(plan.id)}
                  className={`mt-8 w-full rounded-md px-4 py-3 text-base font-bold transition ${
                    plan.highlight
                      ? "bg-blue-600 text-white hover:bg-blue-500"
                      : "bg-slate-700 text-white hover:bg-slate-600"
                  } disabled:cursor-not-allowed disabled:opacity-70`}
                >
                  {isLoading ? `Processing ${plan.title}...` : `Choose ${plan.title}`}
                </button>
              </section>
            );
          })}
        </div>
      </div>
    </div>
  );
}
