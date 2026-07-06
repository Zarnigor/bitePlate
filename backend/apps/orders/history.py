from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import Iterator, List, Optional

from core.patterns.singleton import SingletonMeta


@dataclass
class OrderRecord:
    """Immutable record stored in OrderHistoryLog."""
    order_id: UUID
    table_id: UUID
    staff_id: UUID
    status: str
    total: Decimal
    item_count: int
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def get_audit_entry(self) -> dict:
        return {
            "order_id": str(self.order_id),
            "table_id": str(self.table_id),
            "staff_id": str(self.staff_id),
            "status": self.status,
            "total": float(self.total),
            "item_count": self.item_count,
            "timestamp": self.timestamp.isoformat(),
        }


class OrderHistoryLog(metaclass=SingletonMeta):
    """
    Global in-memory order history log.
    Pattern #6: Singleton Pattern — only one instance can ever exist.
    Pattern: Iterator — supports for-loop iteration over records.

    Note: In production, complement with DB persistence.
    """

    def __init__(self) -> None:
        self._records: List[OrderRecord] = []

    def append(self, record: OrderRecord) -> None:
        self._records.append(record)

    def get_by_table(self, table_id: UUID) -> List[OrderRecord]:
        return [r for r in self._records if r.table_id == table_id]

    def get_by_date(self, date: datetime) -> List[OrderRecord]:
        return [r for r in self._records if r.timestamp.date() == date.date()]

    def get_revenue_summary(self) -> dict:
        total = sum(r.total for r in self._records)
        count = len(self._records)
        return {
            "total_revenue": float(total),
            "order_count": count,
            "average_order": float(total / count) if count else 0,
        }

    def get_all(self) -> List[OrderRecord]:
        return list(self._records)

    def clear(self) -> None:
        """Used in tests only."""
        self._records.clear()

    # Iterator protocol
    def __iter__(self) -> Iterator[OrderRecord]:
        return iter(self._records)

    def __len__(self) -> int:
        return len(self._records)
