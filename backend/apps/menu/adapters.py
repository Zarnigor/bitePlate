from decimal import Decimal
from core.patterns.decorator import MenuItemComponent
from .models import MenuItem


class DjangoMenuItemAdapter(MenuItemComponent):
    """
    Adapter — wraps a Django MenuItem ORM instance
    to satisfy the MenuItemComponent interface used by decorators.
    """

    def __init__(self, model: MenuItem) -> None:
        self._model = model

    def get_price(self) -> Decimal:
        return self._model.get_price()

    def get_display_name(self) -> str:
        return self._model.get_display_name()

    def get_allergens(self) -> list[str]:
        return self._model.get_allergens()
