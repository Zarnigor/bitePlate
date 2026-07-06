import uuid
from decimal import Decimal
from django.db import models


class Bill(models.Model):
    """
    Generated bill for an order.
    Demonstrates: Encapsulation, Facade (BillingFacade generates this)
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.UUIDField(unique=True)
    table_id = models.UUIDField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0"))
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tip_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0"))
    total = models.DecimalField(max_digits=10, decimal_places=2)
    pricing_strategy = models.CharField(max_length=100, default="Standard")
    is_paid = models.BooleanField(default=False)
    split_count = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def per_person_amount(self) -> Decimal:
        if self.split_count < 1:
            return self.total
        return (self.total / self.split_count).quantize(Decimal("0.01"))

    def __str__(self) -> str:
        return f"Bill for Order {self.order_id} — ${self.total} [{self.pricing_strategy}]"
