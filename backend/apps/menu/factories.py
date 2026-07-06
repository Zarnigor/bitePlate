from typing import Any, Dict
from core.patterns.factory import MenuItemFactory
from .models import MenuItem, Category


class StarterFactory(MenuItemFactory):
    """Pattern #4: Factory Method — creates Starter items."""

    def create(self, data: Dict[str, Any]) -> MenuItem:
        data["category"] = Category.STARTER
        data.setdefault("prep_time_seconds", 300)   # starters are quick
        data.setdefault("cooking_station", "cold_kitchen")
        item = MenuItem(**data)
        item.save()
        return item


class MainCourseFactory(MenuItemFactory):
    """Pattern #4: Factory Method — creates Main Course items."""

    def create(self, data: Dict[str, Any]) -> MenuItem:
        data["category"] = Category.MAIN
        data.setdefault("prep_time_seconds", 900)
        data.setdefault("cooking_station", "hot_kitchen")
        item = MenuItem(**data)
        item.save()
        return item


class DessertFactory(MenuItemFactory):
    """Pattern #4: Factory Method — creates Dessert items."""

    def create(self, data: Dict[str, Any]) -> MenuItem:
        data["category"] = Category.DESSERT
        data.setdefault("prep_time_seconds", 600)
        data.setdefault("cooking_station", "pastry")
        item = MenuItem(**data)
        item.save()
        return item


class BeverageFactory(MenuItemFactory):
    """Pattern #4: Factory Method — creates Beverage items."""

    def create(self, data: Dict[str, Any]) -> MenuItem:
        data["category"] = Category.BEVERAGE
        data.setdefault("prep_time_seconds", 60)
        data.setdefault("cooking_station", "bar")
        item = MenuItem(**data)
        item.save()
        return item
