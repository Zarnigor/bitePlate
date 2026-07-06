"""
Unit tests for all 6 Design Patterns.
Run: pytest tests/ -v
"""

import pytest
from decimal import Decimal
from unittest.mock import MagicMock, patch


# ─────────────────────────────────────────────────────────────
# Pattern #1: Command
# ─────────────────────────────────────────────────────────────
class TestCommandPattern:
    def test_execute_adds_to_history(self):
        from core.patterns.command import KitchenQueue, Command

        queue = KitchenQueue()

        class MockCommand(Command):
            executed = False
            undone = False
            def execute(self): self.executed = True
            def undo(self): self.undone = True

        cmd = MockCommand()
        queue.execute(cmd)
        assert cmd.executed is True
        assert queue.history_count == 1

    def test_undo_removes_from_history(self):
        from core.patterns.command import KitchenQueue, Command

        queue = KitchenQueue()

        class MockCommand(Command):
            undone = False
            def execute(self): pass
            def undo(self): self.undone = True

        cmd = MockCommand()
        queue.execute(cmd)
        queue.undo_last()
        assert cmd.undone is True
        assert queue.history_count == 0

    def test_undo_empty_queue_does_nothing(self):
        from core.patterns.command import KitchenQueue
        queue = KitchenQueue()
        queue.undo_last()  # should not raise


# ─────────────────────────────────────────────────────────────
# Pattern #2: Observer
# ─────────────────────────────────────────────────────────────
class TestObserverPattern:
    def test_all_observers_notified(self):
        from core.patterns.observer import Subject, Observer

        class MockObserver(Observer):
            def __init__(self): self.events = []
            def update(self, event, data): self.events.append(event)

        subject = Subject()
        obs1, obs2 = MockObserver(), MockObserver()
        subject.attach(obs1)
        subject.attach(obs2)
        subject.notify("TEST_EVENT", {})

        assert "TEST_EVENT" in obs1.events
        assert "TEST_EVENT" in obs2.events

    def test_detach_stops_notifications(self):
        from core.patterns.observer import Subject, Observer

        class MockObserver(Observer):
            def __init__(self): self.called = False
            def update(self, event, data): self.called = True

        subject = Subject()
        obs = MockObserver()
        subject.attach(obs)
        subject.detach(obs)
        subject.notify("EVENT", {})
        assert obs.called is False


# ─────────────────────────────────────────────────────────────
# Pattern #3: Strategy
# ─────────────────────────────────────────────────────────────
class TestStrategyPattern:
    def test_standard_no_discount(self):
        from core.patterns.strategy import StandardPricing
        assert StandardPricing().calculate(Decimal("100")) == Decimal("100")

    def test_happy_hour_20_percent_off(self):
        from core.patterns.strategy import HappyHourPricing
        result = HappyHourPricing().calculate(Decimal("100"))
        assert result == Decimal("80")

    def test_loyalty_10_percent_off(self):
        from core.patterns.strategy import LoyaltyCardPricing
        result = LoyaltyCardPricing().calculate(Decimal("100"))
        assert result == Decimal("90")

    def test_group_15_percent_off(self):
        from core.patterns.strategy import GroupDiscountPricing
        result = GroupDiscountPricing().calculate(Decimal("100"))
        assert result == Decimal("85")

    def test_strategies_interchangeable(self):
        """Same interface — strategies are interchangeable."""
        from core.patterns.strategy import (
            StandardPricing, HappyHourPricing, LoyaltyCardPricing
        )
        subtotal = Decimal("50")
        for Strategy in [StandardPricing, HappyHourPricing, LoyaltyCardPricing]:
            result = Strategy().calculate(subtotal)
            assert isinstance(result, Decimal)


# ─────────────────────────────────────────────────────────────
# Pattern #4: Factory Method
# ─────────────────────────────────────────────────────────────
class TestFactoryMethod:
    def test_unknown_category_raises(self):
        from core.patterns.factory import MenuItemFactory
        with pytest.raises(ValueError, match="Unknown menu category"):
            MenuItemFactory.get_factory("pizza_thing")

    def test_returns_correct_factory_type(self):
        from core.patterns.factory import MenuItemFactory
        from apps.menu.factories import StarterFactory, BeverageFactory
        assert isinstance(MenuItemFactory.get_factory("starter"), StarterFactory)
        assert isinstance(MenuItemFactory.get_factory("beverage"), BeverageFactory)


# ─────────────────────────────────────────────────────────────
# Pattern #5: Decorator
# ─────────────────────────────────────────────────────────────
class TestDecoratorPattern:
    def _make_base(self, price=Decimal("10.00"), name="Pasta"):
        from core.patterns.decorator import MenuItemComponent

        class FakeItem(MenuItemComponent):
            def get_price(self): return price
            def get_display_name(self): return name
            def get_allergens(self): return []

        return FakeItem()

    def test_extra_ingredient_adds_price(self):
        from core.patterns.decorator import ExtraIngredientDecorator
        base = self._make_base(Decimal("10.00"))
        decorated = ExtraIngredientDecorator(base, "Cheese", Decimal("2.00"))
        assert decorated.get_price() == Decimal("12.00")

    def test_allergen_flag_no_price_change(self):
        from core.patterns.decorator import AllergenFlagDecorator
        base = self._make_base(Decimal("10.00"))
        decorated = AllergenFlagDecorator(base, "Gluten")
        assert decorated.get_price() == Decimal("10.00")
        assert "Gluten" in decorated.get_allergens()

    def test_multiple_decorators_stack(self):
        from core.patterns.decorator import (
            ExtraIngredientDecorator, AllergenFlagDecorator, SpecialNoteDecorator
        )
        base = self._make_base(Decimal("10.00"), "Salad")
        d = ExtraIngredientDecorator(base, "Avocado", Decimal("3.00"))
        d = AllergenFlagDecorator(d, "Nuts")
        d = SpecialNoteDecorator(d, "no dressing")
        assert d.get_price() == Decimal("13.00")
        assert "Nuts" in d.get_allergens()
        assert "no dressing" in d.get_display_name()


# ─────────────────────────────────────────────────────────────
# Pattern #6: Singleton
# ─────────────────────────────────────────────────────────────
class TestSingletonPattern:
    def test_same_instance_returned(self):
        from apps.orders.history import OrderHistoryLog
        a = OrderHistoryLog()
        b = OrderHistoryLog()
        assert a is b

    def test_data_persists_across_instances(self):
        from apps.orders.history import OrderHistoryLog, OrderRecord
        from uuid import uuid4
        from datetime import datetime

        log = OrderHistoryLog()
        log.clear()

        record = OrderRecord(
            order_id=uuid4(),
            table_id=uuid4(),
            staff_id=uuid4(),
            status="confirmed",
            total=Decimal("45.00"),
            item_count=3,
            timestamp=datetime.utcnow(),
        )
        log.append(record)

        # Get a "different" instance — should be same
        log2 = OrderHistoryLog()
        assert len(log2) == 1

        log.clear()  # cleanup
