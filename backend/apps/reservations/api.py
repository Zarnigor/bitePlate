from datetime import datetime, timedelta
from uuid import UUID
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from .models import Reservation, ReservationStatus
from apps.tables.models import Table

router = APIRouter(prefix="/reservations", tags=["Reservations"])


class ReservationCreate(BaseModel):
    table_id: UUID
    customer_name: str
    customer_phone: str = ""
    party_size: int
    reserved_at: datetime
    notes: str = ""


@router.post("/", status_code=201)
def create_reservation(body: ReservationCreate):
    # Check table is free at that time
    try:
        table = Table.objects.get(id=body.table_id)
    except Table.DoesNotExist:
        raise HTTPException(status_code=404, detail="Table not found")

    reservation = Reservation.objects.create(**body.model_dump())
    table.reserve()

    # Schedule reminder — 2 hours before
    reminder_time = body.reserved_at - timedelta(hours=2)
    from infrastructure.celery_app.tasks import send_reservation_reminder
    send_reservation_reminder.apply_async(
        args=[str(reservation.id)],
        eta=reminder_time,
    )

    return {
        "id": str(reservation.id),
        "status": reservation.status,
        "reserved_at": reservation.reserved_at.isoformat(),
        "reminder_scheduled": reminder_time.isoformat(),
    }


@router.get("/")
def list_reservations(date: Optional[str] = None):
    qs = Reservation.objects.all()
    if date:
        d = datetime.fromisoformat(date).date()
        qs = qs.filter(reserved_at__date=d)
    return [
        {
            "id": r.id,
            "customer_name": r.customer_name,
            "party_size": r.party_size,
            "reserved_at": r.reserved_at.isoformat(),
            "status": r.status,
            "table_id": r.table_id,
        }
        for r in qs
    ]


@router.post("/{reservation_id}/arrive")
def mark_arrived(reservation_id: UUID):
    try:
        r = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        raise HTTPException(status_code=404)
    r.status = ReservationStatus.ARRIVED
    r.save(update_fields=["status"])
    # Seat the table
    table = Table.objects.get(id=r.table_id)
    table.seat()
    return {"status": r.status}
