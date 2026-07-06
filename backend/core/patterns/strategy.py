from abc import ABC, abstractmethod
from decimal import Decimal


class PricingStrategy(ABC):
    """Abstract Strategy — Pattern #3: Strategy Pattern"""

    @abstractmethod
    def calculate(self, subtotal: Decimal) -> Decimal:
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        ...


class StandardPricing(PricingStrategy):
    """No discount — full price."""

    def calculate(self, subtotal: Decimal) -> Decimal:
        return subtotal

    @property
    def name(self) -> str:
        return "Standard"


class HappyHourPricing(PricingStrategy):
    """20% discount during happy hour."""

    DISCOUNT = Decimal("0.80")

    def calculate(self, subtotal: Decimal) -> Decimal:
        return subtotal * self.DISCOUNT

    @property
    def name(self) -> str:
        return "Happy Hour (20% off)"


class LoyaltyCardPricing(PricingStrategy):
    """10% discount for loyalty card holders."""

    DISCOUNT = Decimal("0.90")

    def calculate(self, subtotal: Decimal) -> Decimal:
        return subtotal * self.DISCOUNT

    @property
    def name(self) -> str:
        return "Loyalty Card (10% off)"


class GroupDiscountPricing(PricingStrategy):
    """15% discount for groups of 8+."""

    DISCOUNT = Decimal("0.85")

    def calculate(self, subtotal: Decimal) -> Decimal:
        return subtotal * self.DISCOUNT

    @property
    def name(self) -> str:
        return "Group Discount (15% off)"
