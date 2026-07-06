from abc import ABC, abstractmethod
from decimal import Decimal


class MenuItemComponent(ABC):
    """
    Abstract Component — Pattern #5: Decorator Pattern
    Both concrete items and decorators implement this interface.
    """

    @abstractmethod
    def get_price(self) -> Decimal:
        ...

    @abstractmethod
    def get_display_name(self) -> str:
        ...

    @abstractmethod
    def get_allergens(self) -> list[str]:
        ...


class MenuItemDecorator(MenuItemComponent, ABC):
    """
    Base Decorator — wraps a MenuItemComponent.
    Pattern #5: Decorator Pattern
    """

    def __init__(self, component: MenuItemComponent) -> None:
        self._component = component

    def get_price(self) -> Decimal:
        return self._component.get_price()

    def get_display_name(self) -> str:
        return self._component.get_display_name()

    def get_allergens(self) -> list[str]:
        return self._component.get_allergens()


class AllergenFlagDecorator(MenuItemDecorator):
    """Tags a menu item with an allergen warning (no price change)."""

    def __init__(self, component: MenuItemComponent, allergen: str) -> None:
        super().__init__(component)
        self._allergen = allergen

    def get_allergens(self) -> list[str]:
        return self._component.get_allergens() + [self._allergen]

    def get_display_name(self) -> str:
        return f"{self._component.get_display_name()} ⚠️ [{self._allergen}]"


class ExtraIngredientDecorator(MenuItemDecorator):
    """Adds an extra ingredient with an additional charge."""

    def __init__(
        self,
        component: MenuItemComponent,
        ingredient: str,
        extra_cost: Decimal,
    ) -> None:
        super().__init__(component)
        self._ingredient = ingredient
        self._extra_cost = extra_cost

    def get_price(self) -> Decimal:
        return self._component.get_price() + self._extra_cost

    def get_display_name(self) -> str:
        return f"{self._component.get_display_name()} + {self._ingredient}"


class SpecialNoteDecorator(MenuItemDecorator):
    """Attaches a preparation note (e.g. 'extra spicy', 'no salt')."""

    def __init__(self, component: MenuItemComponent, note: str) -> None:
        super().__init__(component)
        self._note = note

    def get_display_name(self) -> str:
        return f"{self._component.get_display_name()} ({self._note})"
