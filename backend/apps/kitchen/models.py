import uuid
from django.db import models


class KitchenItemStatus(models.TextChoices):
    QUEUED = "queued", "Queued"
    PREPARING = "preparing", "Preparing"
    READY = "ready", "Ready"
    CANCELLED = "cancelled", "Cancelled"


class KitchenTicket(models.Model):
    """
    Represents a kitchen work ticket for one OrderItem.
    Demonstrates: State transitions, Encapsulation
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.UUIDField()
    order_item_id = models.UUIDField()
    item_name = models.CharField(max_length=200)
    station = models.CharField(max_length=100, default="hot_kitchen")
    status = models.CharField(
        max_length=20,
        choices=KitchenItemStatus.choices,
        default=KitchenItemStatus.QUEUED,
    )
    quantity = models.PositiveIntegerField(default=1)
    special_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"[{self.station}] {self.item_name} × {self.quantity} — {self.status}"
