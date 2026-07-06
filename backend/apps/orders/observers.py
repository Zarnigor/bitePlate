from typing import Any, Dict
from core.patterns.observer import Observer


class WaiterNotifier(Observer):
    def __init__(self, waiter_id: str) -> None:
        self.waiter_id = waiter_id
        self.notifications: list[dict] = []

    def update(self, event: str, data: Dict[str, Any]) -> None:
        if event in ("ORDER_SERVED", "ITEM_READY", "ORDER_CONFIRMED", "ORDER_IN_KITCHEN"):
            self.notifications.append({"event": event, "data": data, "for": self.waiter_id})
            print(f"[WAITER {self.waiter_id}] {event}: {data}")


class KitchenNotifier(Observer):
    def update(self, event: str, data: Dict[str, Any]) -> None:
        if event == "ORDER_CONFIRMED":
            print(f"[KITCHEN] New order: {data}")
            try:
                from infrastructure.celery_app.tasks import notify_kitchen_on_order
                notify_kitchen_on_order.delay(data["order_id"])
            except Exception as e:
                print(f"[KITCHEN] Celery task failed: {e}")
        elif event == "ORDER_CANCELLED":
            print(f"[KITCHEN] Cancelled: {data}")


class ManagerDashboard(Observer):
    def __init__(self) -> None:
        self.event_log: list[dict] = []

    def update(self, event: str, data: Dict[str, Any]) -> None:
        self.event_log.append({"event": event, "data": data})
        print(f"[MANAGER] {event}: {data}")
