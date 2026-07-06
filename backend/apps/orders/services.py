from datetime import datetime
from uuid import UUID
from typing import List

from .models import Order, OrderItem, OrderStatus
from .history import OrderHistoryLog, OrderRecord
from .observers import WaiterNotifier, KitchenNotifier, ManagerDashboard


class OrderService:
    """Application layer — all order use cases."""

    def __init__(self) -> None:
        self._log = OrderHistoryLog()
        self._kitchen_notifier = KitchenNotifier()
        self._manager_dashboard = ManagerDashboard()

    def _build_order_with_observers(self, order: Order, waiter_id: str) -> Order:
        order.attach(WaiterNotifier(waiter_id))
        order.attach(self._kitchen_notifier)
        order.attach(self._manager_dashboard)
        return order

    def create_order(self, table_id: UUID, staff_id: UUID, items_data: List[dict]) -> Order:
        """Create a DRAFT order with items."""
        order = Order.objects.create(table_id=table_id, staff_id=staff_id)
        for item in items_data:
            OrderItem.objects.create(
                order=order,
                menu_item_id=item["menu_item_id"],
                menu_item_name=item["name"],
                unit_price=item["unit_price"],
                quantity=item.get("quantity", 1),
                special_notes=item.get("special_notes", ""),
            )
        return order

    def confirm_order(self, order_id: UUID, waiter_id: str) -> Order:
        order = Order.objects.prefetch_related("items").get(id=order_id)
        order = self._build_order_with_observers(order, waiter_id)
        order.confirm()

        # Log to Singleton
        self._log.append(OrderRecord(
            order_id=order.id,
            table_id=order.table_id,
            staff_id=order.staff_id,
            status=order.status,
            total=order.get_subtotal(),
            item_count=order.items.count(),
            timestamp=datetime.utcnow(),
        ))
        return order

    def cancel_order(self, order_id: UUID, waiter_id: str) -> Order:
        order = Order.objects.get(id=order_id)
        order = self._build_order_with_observers(order, waiter_id)
        order.cancel()
        return order

    def mark_served(self, order_id: UUID) -> Order:
        order = Order.objects.get(id=order_id)
        order.mark_served()
        return order

    def get_history_summary(self) -> dict:
        return self._log.get_revenue_summary()

    def get_all_history(self) -> list:
        return [r.get_audit_entry() for r in self._log]

    def get_order(self, order_id: UUID) -> Order:
        return Order.objects.prefetch_related("items").get(id=order_id)
