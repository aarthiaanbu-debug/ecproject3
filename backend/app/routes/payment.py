from fastapi import APIRouter
from pydantic import BaseModel

from app.services.stripe_service import create_checkout_session


router = APIRouter(tags=["payment"])


class CheckoutSessionRequest(BaseModel):
    plan: str


@router.post("/create-checkout-session")
def checkout_session(payload: CheckoutSessionRequest):
    return create_checkout_session(payload.plan)
