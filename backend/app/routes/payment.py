from fastapi import APIRouter, Body
import stripe

router = APIRouter()

stripe.api_key = "sk_test_xxx"

PRICE_MAP = {
    "pro": 49900,
    "premium": 99900
}

@router.post("/create-checkout-session")
def create_checkout_session(data: dict = Body(...)):

    plan = data.get("plan")

    if plan not in PRICE_MAP:
        return {"error": "Invalid plan"}

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",

        line_items=[{
            "price_data": {
                "currency": "inr",
                "product_data": {
                    "name": f"{plan.upper()} PLAN"
                },
                "unit_amount": PRICE_MAP[plan],
            },
            "quantity": 1,
        }],

        success_url="http://localhost:5173/success",
        cancel_url="http://localhost:5173/cancel",

        metadata={"plan": plan}
    )

    return {"url": session.url}