import json

from fastapi import APIRouter, HTTPException, Request, status
import stripe

from app.config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET

router = APIRouter(tags=["stripe"])

@router.post("/stripe-webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stripe webhook payload is empty.",
        )

    if STRIPE_SECRET_KEY:
        stripe.api_key = STRIPE_SECRET_KEY

    if STRIPE_WEBHOOK_SECRET:
        signature = request.headers.get("stripe-signature")

        try:
            event = stripe.Webhook.construct_event(
                payload=payload,
                sig_header=signature,
                secret=STRIPE_WEBHOOK_SECRET,
            )
        except (ValueError, stripe.error.SignatureVerificationError) as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Stripe webhook payload",
            ) from exc
    else:
        try:
            event = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Stripe webhook JSON payload.",
            ) from exc

    return {"received": True, "type": event.get("type")}
