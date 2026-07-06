from decimal import Decimal
from uuid import UUID
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .facade import BillingFacade

router = APIRouter(prefix="/billing", tags=["Billing"])
_facade = BillingFacade()


class GenerateBillRequest(BaseModel):
    strategy: str = "standard"
    tip_pct: Decimal = Decimal("0")
    split_count: int = 1


@router.post("/generate/{order_id}")
def generate_bill(order_id: UUID, body: GenerateBillRequest):
    """
    Generate a bill using the selected pricing strategy (Facade + Strategy patterns).
    strategy options: standard | happy_hour | loyalty | group
    """
    try:
        bill = _facade.generate_bill(
            order_id=order_id,
            strategy_key=body.strategy,
            tip_pct=body.tip_pct,
            split_count=body.split_count,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "bill_id": str(bill.id),
        "subtotal": float(bill.subtotal),
        "discount": float(bill.discount_amount),
        "tax": float(bill.tax_amount),
        "tip": float(bill.tip_amount),
        "total": float(bill.total),
        "per_person": float(bill.per_person_amount()),
        "strategy": bill.pricing_strategy,
        "split_count": bill.split_count,
    }


@router.post("/pay/{bill_id}")
def pay_bill(bill_id: UUID):
    """Mark bill as paid and close the order."""
    try:
        bill = _facade.mark_paid(bill_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"bill_id": str(bill.id), "is_paid": bill.is_paid}


@router.get("/strategies")
def list_strategies():
    return {"strategies": _facade.available_strategies()}
