import uuid
from decimal import Decimal
from django.db import models
from core.patterns.observer import Subject


class OrderStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    CONFIRMED = "confirmed", "Confirmed"
    IN_KITCHEN = "in_kitchen", "In Kitchen"
    SERVED = "served", "Served"
    AWAITING_BILL = "awaiting_bill", "Awaiting Bill"
    CANCELLED = "cancelled", "Cancelled"
    CLOSED = "closed", "Closed"


class Order(models.Model, Subject):
    """
    Core Order entity.
    Demonstrates:
      - Observer Pattern (Subject mixin)
      - Encapsulation (status transitions via methods)
      - Polymorphism (status property with transition guards)
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    table_id = models.UUIDField()
    staff_id = models.UUIDField()
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.DRAFT,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __init__(self, *args, **kwargs):
        # Django models don't call super().__init__ through MRO cleanly
        # so we initialise Subject manually.
        Subject.__init__(self)
        models.Model.__init__(self, *args, **kwargs)

    def get_subtotal(self) -> Decimal:
        return sum(item.get_line_total() for item in self.items.all())

    # ── State transitions ─────────────────────────────────────

    def confirm(self) -> None:
        if self.status != OrderStatus.DRAFT:
            raise ValueError("Only DRAFT orders can be confirmed.")
        self.status = OrderStatus.CONFIRMED
        self.save(update_fields=["status"])
        self.notify("ORDER_CONFIRMED", {"order_id": str(self.id), "table_id": str(self.table_id)})

    def send_to_kitchen(self) -> None:
        if self.status != OrderStatus.CONFIRMED:
            raise ValueError("Only CONFIRMED orders can go to kitchen.")
        self.status = OrderStatus.IN_KITCHEN
        self.save(update_fields=["status"])
        self.notify("ORDER_IN_KITCHEN", {"order_id": str(self.id)})

    def mark_served(self) -> None:
        self.status = OrderStatus.SERVED
        self.save(update_fields=["status"])
        self.notify("ORDER_SERVED", {"order_id": str(self.id), "table_id": str(self.table_id)})

    def request_bill(self) -> None:
        self.status = OrderStatus.AWAITING_BILL
        self.save(update_fields=["status"])
        self.notify("BILL_REQUESTED", {"order_id": str(self.id)})

    def cancel(self) -> None:
        if self.status in (OrderStatus.SERVED, OrderStatus.CLOSED):
            raise ValueError("Cannot cancel a served or closed order.")
        self.status = OrderStatus.CANCELLED
        self.save(update_fields=["status"])
        self.notify("ORDER_CANCELLED", {"order_id": str(self.id)})

    def close(self) -> None:
        self.status = OrderStatus.CLOSED
        self.save(update_fields=["status"])

    def __str__(self) -> str:
        return f"Order {self.id} — Table {self.table_id} [{self.status}]"


class OrderItem(models.Model):
    """
    A single line in an order.
    Demonstrates: Composition with Order (Order *-- OrderItem)
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    menu_item_id = models.UUIDField()
    menu_item_name = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    special_notes = models.TextField(blank=True)

    def get_line_total(self) -> Decimal:
        return self.unit_price * self.quantity

    def __str__(self) -> str:
        return f"{self.quantity}× {self.menu_item_name} @ ${self.unit_price}"
