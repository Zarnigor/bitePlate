from uuid import UUID
from fastapi import APIRouter, HTTPException
from .services import KitchenService

router = APIRouter(prefix="/kitchen", tags=["Kitchen"])
_service = KitchenService()


@router.get("/queue")
def get_queue():
    tickets = _service.get_queue()
    return [
        {
            "id": t.id,
            "order_id": t.order_id,
            "item_name": t.item_name,
            "quantity": t.quantity,
            "station": t.station,
            "status": t.status,
            "special_notes": t.special_notes,
            "created_at": t.created_at.isoformat(),
        }
        for t in tickets
    ]


@router.post("/tickets/{ticket_id}/prepare")
def prepare(ticket_id: UUID):
    """Execute PrepareTicketCommand."""
    try:
        ticket = _service.prepare(ticket_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"ticket_id": str(ticket.id), "status": ticket.status}


@router.post("/tickets/{ticket_id}/ready")
def mark_ready(ticket_id: UUID):
    """Execute MarkReadyCommand — notifies waiter."""
    try:
        ticket = _service.mark_ready(ticket_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"ticket_id": str(ticket.id), "status": ticket.status}


@router.post("/tickets/{ticket_id}/cancel")
def cancel(ticket_id: UUID):
    """Execute CancelTicketCommand."""
    try:
        ticket = _service.cancel_ticket(ticket_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"ticket_id": str(ticket.id), "status": ticket.status}


@router.post("/undo")
def undo():
    """Undo the last kitchen command."""
    _service.undo_last()
    return {"message": "Last kitchen command undone."}
