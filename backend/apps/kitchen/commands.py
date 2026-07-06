from uuid import UUID
from core.patterns.command import Command, KitchenQueue
from .models import KitchenTicket, KitchenItemStatus


class PrepareTicketCommand(Command):
    def __init__(self, ticket: KitchenTicket) -> None:
        self._ticket = ticket
        self._previous_status = ticket.status

    def execute(self) -> None:
        self._previous_status = self._ticket.status
        self._ticket.status = KitchenItemStatus.PREPARING
        self._ticket.save(update_fields=["status"])

    def undo(self) -> None:
        self._ticket.status = self._previous_status
        self._ticket.save(update_fields=["status"])


class MarkReadyCommand(Command):
    def __init__(self, ticket: KitchenTicket) -> None:
        self._ticket = ticket
        self._previous_status = ticket.status

    def execute(self) -> None:
        self._previous_status = self._ticket.status
        self._ticket.status = KitchenItemStatus.READY
        self._ticket.save(update_fields=["status"])
        try:
            from infrastructure.celery_app.tasks import broadcast_order_status
            broadcast_order_status.delay(
                str(self._ticket.order_id), "ITEM_READY",
                {"item": self._ticket.item_name, "ticket_id": str(self._ticket.id)},
            )
        except Exception:
            pass

    def undo(self) -> None:
        self._ticket.status = self._previous_status
        self._ticket.save(update_fields=["status"])


class CancelTicketCommand(Command):
    def __init__(self, ticket: KitchenTicket) -> None:
        self._ticket = ticket
        self._previous_status = ticket.status

    def execute(self) -> None:
        self._previous_status = self._ticket.status
        self._ticket.status = KitchenItemStatus.CANCELLED
        self._ticket.save(update_fields=["status"])

    def undo(self) -> None:
        self._ticket.status = self._previous_status
        self._ticket.save(update_fields=["status"])


kitchen_queue = KitchenQueue()
