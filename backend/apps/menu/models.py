import uuid
from decimal import Decimal
from django.db import models


class Category(models.TextChoices):
    STARTER = "starter", "Starter"
    MAIN = "main", "Main Course"
    DESSERT = "dessert", "Dessert"
    BEVERAGE = "beverage", "Beverage"


class MenuItem(models.Model):
    """
    Base menu item model.
    Demonstrates: Encapsulation (private fields + properties),
    Abstraction (get_price, get_display_name polymorphic via category)
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=20, choices=Category.choices)
    is_available = models.BooleanField(default=True)
    prep_time_seconds = models.PositiveIntegerField(default=600)
    cooking_station = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.category}) — ${self.base_price}"

    def get_price(self) -> Decimal:
        """Polymorphic price resolution — overridden by ComboMeal."""
        return self.base_price

    def get_display_name(self) -> str:
        return self.name

    def get_allergens(self) -> list[str]:
        return list(self.allergens.values_list("name", flat=True))


class Allergen(models.Model):
    """Allergen master list."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    menu_item = models.ForeignKey(
        MenuItem,
        related_name="allergens",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return self.name


class ComboMeal(MenuItem):
    """
    Composite Pattern — a ComboMeal IS-A MenuItem and contains many MenuItems.
    Pattern #5: Composite (extends Decorator chain)
    Demonstrates: Inheritance, Polymorphism (get_price overridden)
    """

    discount_pct = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("10.00"),
        help_text="Discount percentage applied to sum of item prices.",
    )
    items = models.ManyToManyField(
        MenuItem,
        related_name="combo_meals",
        blank=True,
    )

    def get_price(self) -> Decimal:
        """Override: sum of items minus discount."""
        total = sum(item.get_price() for item in self.items.all())
        discount_factor = 1 - (self.discount_pct / Decimal("100"))
        return (total * discount_factor).quantize(Decimal("0.01"))

    def get_display_name(self) -> str:
        return f"🍱 {self.name} (Combo)"
