from decimal import Decimal
from typing import Any, Dict, Optional
from uuid import UUID

from core.patterns.factory import MenuItemFactory
from core.patterns.decorator import (
    AllergenFlagDecorator,
    ExtraIngredientDecorator,
    SpecialNoteDecorator,
    MenuItemComponent,
)
from .models import MenuItem, ComboMeal, Allergen
from .schemas import MenuItemCreate, ComboMealCreate, CustomisationRequest


class MenuService:
    """Application layer — all menu use cases."""

    # ── Factory Method ────────────────────────────────────────
    def create_menu_item(self, data: MenuItemCreate) -> MenuItem:
        """Use Factory Method to create the correct item type by category."""
        factory = MenuItemFactory.get_factory(data.category)
        return factory.create(data.model_dump(exclude={"category"}))

    # ── Composite ─────────────────────────────────────────────
    def create_combo(self, data: ComboMealCreate) -> ComboMeal:
        items = MenuItem.objects.filter(id__in=data.item_ids)
        combo = ComboMeal.objects.create(
            name=data.name,
            description=data.description,
            discount_pct=data.discount_pct,
            category="main",
            base_price=Decimal("0"),
        )
        combo.items.set(items)
        return combo

    # ── Decorator Pattern ─────────────────────────────────────
    def customise_item(self, req: CustomisationRequest) -> MenuItemComponent:
        """
        Wrap a MenuItem with Decorator layers at runtime.
        Returns a decorated component (not saved to DB — used for price calc).
        """
        from apps.menu.adapters import DjangoMenuItemAdapter

        base_item = MenuItem.objects.get(id=req.menu_item_id)
        component: MenuItemComponent = DjangoMenuItemAdapter(base_item)

        for allergen in req.allergen_flags:
            component = AllergenFlagDecorator(component, allergen)

        for extra in req.extra_ingredients:
            component = ExtraIngredientDecorator(
                component,
                extra["ingredient"],
                Decimal(str(extra["extra_cost"])),
            )

        if req.special_note:
            component = SpecialNoteDecorator(component, req.special_note)

        return component

    def list_available(self) -> list[MenuItem]:
        return list(MenuItem.objects.filter(is_available=True))

    def toggle_availability(self, item_id: UUID) -> MenuItem:
        item = MenuItem.objects.get(id=item_id)
        item.is_available = not item.is_available
        item.save(update_fields=["is_available"])
        return item
