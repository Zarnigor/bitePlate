from uuid import UUID
from fastapi import APIRouter, HTTPException, Header, status
from .schemas import OrderCreate, OrderResponse, OrderItemResponse
from .services import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])
_service = OrderService()


def _serialize_order(order) -> dict:
    items = [
        OrderItemResponse(
            id=i.id,
            menu_item_name=i.menu_item_name,
            unit_price=i.unit_price,
            quantity=i.quantity,
            line_total=i.get_line_total(),
            special_notes=i.special_notes,
        )
        for i in order.items.all()
    ]
    return OrderResponse(
        id=order.id,
        table_id=order.table_id,
        staff_id=order.staff_id,
        status=order.status,
        subtotal=order.get_subtotal(),
        items=items,
    ).model_dump()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_order(body: OrderCreate):
    order = _service.create_order(
        table_id=body.table_id,
        staff_id=body.staff_id,
        items_data=[i.model_dump() for i in body.items],
    )
    return _serialize_order(order)


@router.get("/{order_id}")
def get_order(order_id: UUID):
    try:
        order = _service.get_order(order_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Order not found")
    return _serialize_order(order)


@router.post("/{order_id}/confirm")
def confirm_order(order_id: UUID, x_staff_id: str = Header(...)):
    """Confirm order — triggers Observer notifications to Kitchen + Manager."""
    try:
        order = _service.confirm_order(order_id, waiter_id=x_staff_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"status": order.status, "order_id": str(order.id)}


@router.post("/{order_id}/cancel")
def cancel_order(order_id: UUID, x_staff_id: str = Header(...)):
    try:
        order = _service.cancel_order(order_id, waiter_id=x_staff_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"status": order.status}


@router.post("/{order_id}/served")
def mark_served(order_id: UUID):
    order = _service.mark_served(order_id)
    return {"status": order.status}


@router.get("/history/summary")
def history_summary():
    return _service.get_history_summary()


@router.get("/history/all")
def history_all():
    return _service.get_all_history()
