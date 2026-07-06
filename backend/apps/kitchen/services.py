from uuid import UUID
from typing import List

from .models import KitchenTicket, KitchenItemStatus
from .commands import (
    PrepareTicketCommand,
    MarkReadyCommand,
    CancelTicketCommand,
    kitchen_queue,
)


class KitchenService:
    """Application layer — kitchen queue use cases."""

    def create_tickets_for_order(self, order_id: UUID, items: List[dict]) -> List[KitchenTicket]:
        """Called by Celery task when an order is confirmed."""
        tickets = []
        for item in items:
            ticket = KitchenTicket.objects.create(
                order_id=order_id,
                order_item_id=item["order_item_id"],
                item_name=item["name"],
                station=item.get("station", "hot_kitchen"),
                quantity=item.get("quantity", 1),
                special_notes=item.get("special_notes", ""),
            )
            tickets.append(ticket)
        return tickets

    def get_queue(self) -> List[KitchenTicket]:
        """Return all non-done tickets sorted by creation time."""
        return list(
            KitchenTicket.objects.filter(
                status__in=[KitchenItemStatus.QUEUED, KitchenItemStatus.PREPARING]
            )
        )

    def prepare(self, ticket_id: UUID) -> KitchenTicket:
        ticket = KitchenTicket.objects.get(id=ticket_id)
        kitchen_queue.execute(PrepareTicketCommand(ticket))
        return ticket

    def mark_ready(self, ticket_id: UUID) -> KitchenTicket:
        ticket = KitchenTicket.objects.get(id=ticket_id)
        kitchen_queue.execute(MarkReadyCommand(ticket))
        return ticket

    def cancel_ticket(self, ticket_id: UUID) -> KitchenTicket:
        ticket = KitchenTicket.objects.get(id=ticket_id)
        kitchen_queue.execute(CancelTicketCommand(ticket))
        return ticket

    def undo_last(self) -> None:
        kitchen_queue.undo_last()
