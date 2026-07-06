import uuid
from django.db import models


class TableStatus(models.TextChoices):
    FREE = "free", "Free"
    RESERVED = "reserved", "Reserved"
    OCCUPIED = "occupied", "Occupied"
    AWAITING_BILL = "awaiting_bill", "Awaiting Bill"
    CLEARED = "cleared", "Cleared (being cleaned)"


class Table(models.Model):
    """
    Demonstrates: Encapsulation (status transitions via methods)
    State machine: FREE → RESERVED → OCCUPIED → AWAITING_BILL → CLEARED → FREE
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField(default=4)
    status = models.CharField(
        max_length=20,
        choices=TableStatus.choices,
        default=TableStatus.FREE,
    )
    location = models.CharField(max_length=100, blank=True, help_text="e.g. window, terrace")

    class Meta:
        ordering = ["number"]

    # ── State transitions ─────────────────────────────────────

    def reserve(self) -> None:
        if self.status != TableStatus.FREE:
            raise ValueError(f"Table {self.number} is not free.")
        self.status = TableStatus.RESERVED
        self.save(update_fields=["status"])

    def seat(self) -> None:
        if self.status not in (TableStatus.RESERVED, TableStatus.FREE):
            raise ValueError(f"Table {self.number} cannot be seated.")
        self.status = TableStatus.OCCUPIED
        self.save(update_fields=["status"])

    def request_bill(self) -> None:
        self.status = TableStatus.AWAITING_BILL
        self.save(update_fields=["status"])

    def clear(self) -> None:
        self.status = TableStatus.FREE
        self.save(update_fields=["status"])

    def __str__(self) -> str:
        return f"Table {self.number} ({self.capacity} pax) — {self.status}"
