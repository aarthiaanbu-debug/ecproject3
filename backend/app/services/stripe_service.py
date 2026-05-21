from fastapi import HTTPException, status
import stripe

from app.config import FRONTEND_URL, STRIPE_SECRET_KEY


PRICE_MAP = {
    "pro": 49900,
    "premium": 99900,
    "gold": 199900,
}


def create_checkout_session(plan: str) -> dict:
    normalized_plan = plan.lower().strip() if plan else ""

    if normalized_plan not in PRICE_MAP:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid plan",
        )

    if not STRIPE_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Stripe is not configured. Set STRIPE_SECRET_KEY in the backend environment.",
        )

    stripe.api_key = STRIPE_SECRET_KEY

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": "inr",
                        "product_data": {
                            "name": f"{normalized_plan.upper()} PLAN",
                        },
                        "unit_amount": PRICE_MAP[normalized_plan],
                    },
                    "quantity": 1,
                }
            ],
            success_url=f"{FRONTEND_URL}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{FRONTEND_URL}/cancel",
            metadata={"plan": normalized_plan},
        )
    except stripe.error.StripeError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc

    return {"url": session.url, "id": session.id}


def get_checkout_session(session_id: str) -> dict:
    if not STRIPE_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Stripe is not configured. Set STRIPE_SECRET_KEY in the backend environment.",
        )

    stripe.api_key = STRIPE_SECRET_KEY

    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except stripe.error.StripeError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc

    return {
        "id": session.id,
        "status": session.status,
        "payment_status": session.payment_status,
        "customer_email": session.customer_details.email
        if session.customer_details
        else None,
        "plan": session.metadata.get("plan") if session.metadata else None,
    }
