from abc import ABC, abstractmethod
from typing import Dict, Any


class MenuItemFactory(ABC):
    """
    Abstract Factory — Pattern #4: Factory Method Pattern
    Subclasses decide which MenuItem type to create.
    """

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> "MenuItem":  # noqa: F821
        ...

    @classmethod
    def get_factory(cls, category: str) -> "MenuItemFactory":
        """Return the correct factory for a given category string."""
        from apps.menu.factories import (
            StarterFactory,
            MainCourseFactory,
            DessertFactory,
            BeverageFactory,
        )

        mapping: Dict[str, MenuItemFactory] = {
            "starter": StarterFactory(),
            "main": MainCourseFactory(),
            "dessert": DessertFactory(),
            "beverage": BeverageFactory(),
        }
        factory = mapping.get(category.lower())
        if factory is None:
            raise ValueError(f"Unknown menu category: {category!r}")
        return factory
