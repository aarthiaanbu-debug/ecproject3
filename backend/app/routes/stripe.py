from fastapi import APIRouter
from pydantic import BaseModel

from app.services.stripe_service import create_checkout_session, get_checkout_session


router = APIRouter(prefix="/stripe", tags=["stripe"])


class CheckoutSessionRequest(BaseModel):
    plan: str
    customer_name: str | None = None


@router.post("/create-checkout-session")
def checkout_session(payload: CheckoutSessionRequest):
    return create_checkout_session(payload.plan, payload.customer_name)


@router.get("/session/{session_id}")
def checkout_session_details(session_id: str):
    return get_checkout_session(session_id)
