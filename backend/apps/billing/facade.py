from decimal import Decimal
from uuid import UUID
from django.conf import settings

from core.patterns.strategy import (
    PricingStrategy, StandardPricing, HappyHourPricing,
    LoyaltyCardPricing, GroupDiscountPricing,
)
from apps.orders.models import Order
from .models import Bill

STRATEGY_MAP: dict[str, PricingStrategy] = {
    "standard":   StandardPricing(),
    "happy_hour": HappyHourPricing(),
    "loyalty":    LoyaltyCardPricing(),
    "group":      GroupDiscountPricing(),
}


class BillingFacade:
    """Facade Pattern — single entry point for all billing logic."""

    def _tax_rate(self) -> Decimal:
        rate = getattr(settings, "DEFAULT_TAX_RATE", "0.12")
        return Decimal(str(rate))

    def generate_bill(self, order_id: UUID, strategy_key: str = "standard",
                      tip_pct: Decimal = Decimal("0"), split_count: int = 1) -> Bill:
        order = Order.objects.prefetch_related("items").get(id=order_id)
        subtotal = order.get_subtotal()
        strategy = STRATEGY_MAP.get(strategy_key, StandardPricing())
        discounted = strategy.calculate(subtotal)
        discount_amount = subtotal - discounted
        tax_amount = (discounted * self._tax_rate()).quantize(Decimal("0.01"))
        tip_amount = (discounted * tip_pct / 100).quantize(Decimal("0.01"))
        total = (discounted + tax_amount + tip_amount).quantize(Decimal("0.01"))
        bill = Bill.objects.create(
            order_id=order.id, table_id=order.table_id,
            subtotal=subtotal, discount_amount=discount_amount,
            tax_amount=tax_amount, tip_amount=tip_amount, total=total,
            pricing_strategy=strategy.name, split_count=split_count,
        )
        order.request_bill()
        return bill

    def mark_paid(self, bill_id: UUID) -> Bill:
        bill = Bill.objects.get(id=bill_id)
        bill.is_paid = True
        bill.save(update_fields=["is_paid"])
        order = Order.objects.get(id=bill.order_id)
        order.close()
        return bill

    def available_strategies(self) -> list[str]:
        return list(STRATEGY_MAP.keys())
