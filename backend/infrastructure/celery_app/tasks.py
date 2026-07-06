from celery import shared_task
from typing import Any


@shared_task(name="kitchen.notify_kitchen_on_order", bind=True, max_retries=3)
def notify_kitchen_on_order(self, order_id: str) -> None:
    """
    Async task: create KitchenTickets for a confirmed order.
    Triggered by: KitchenNotifier (Observer) when ORDER_CONFIRMED fires.
    """
    try:
        from uuid import UUID
        from apps.orders.models import Order
        from apps.kitchen.services import KitchenService

        order = Order.objects.prefetch_related("items").get(id=UUID(order_id))
        items_data = [
            {
                "order_item_id": str(item.id),
                "name": item.menu_item_name,
                "quantity": item.quantity,
                "special_notes": item.special_notes,
            }
            for item in order.items.all()
        ]
        KitchenService().create_tickets_for_order(order.id, items_data)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=5)


@shared_task(name="orders.broadcast_order_status")
def broadcast_order_status(order_id: str, event: str, data: dict) -> None:
    """
    Async task: broadcast real-time status changes via WebSocket / push.
    In production: push to Django Channels or a push notification service.
    """
    print(f"[BROADCAST] {event} for order {order_id}: {data}")


@shared_task(name="reservations.send_reminder", bind=True, max_retries=3)
def send_reservation_reminder(self, reservation_id: str) -> None:
    """
    Async task: send SMS/push reminder 2h before reservation.
    Scheduled with ETA by ReservationService.
    """
    try:
        from uuid import UUID
        from apps.reservations.models import Reservation, ReservationStatus

        r = Reservation.objects.get(id=UUID(reservation_id))
        if r.status in (ReservationStatus.CANCELLED, ReservationStatus.ARRIVED):
            return  # no longer needed

        # In production: call SMS provider (Twilio, Vonage, etc.)
        print(f"[SMS] Reminder to {r.customer_phone}: Your reservation at {r.reserved_at} is in 2 hours.")
        r.reminder_sent = True
        r.save(update_fields=["reminder_sent"])
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@shared_task(name="billing.generate_night_report")
def generate_end_of_night_report() -> dict:
    """
    Periodic Celery Beat task — runs daily at 23:59.
    Iterates OrderHistoryLog (Singleton + Iterator patterns).
    """
    from apps.orders.history import OrderHistoryLog

    log = OrderHistoryLog()
    summary = log.get_revenue_summary()
    records = log.get_all()

    # Per-staff breakdown
    staff_covers: dict[str, int] = {}
    for record in records:
        sid = str(record.staff_id)
        staff_covers[sid] = staff_covers.get(sid, 0) + 1

    top_staff = sorted(staff_covers.items(), key=lambda x: x[1], reverse=True)[:3]

    report = {
        "date": records[-1].timestamp.date().isoformat() if records else "N/A",
        "total_revenue": summary["total_revenue"],
        "order_count": summary["order_count"],
        "average_order": summary["average_order"],
        "top_staff": top_staff,
    }

    print(f"[NIGHT REPORT] {report}")
    return report
