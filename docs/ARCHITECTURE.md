# BitePlate — Architecture & Design Patterns

## Overview

BitePlate is a **Smart Restaurant Management System** built with Django + FastAPI, following **Clean Architecture** principles. The system is divided into independent modules (Django apps) that can be extracted into microservices.

---

## Clean Architecture Layers

```
┌─────────────────────────────────────────────┐
│              API Layer (FastAPI/DRF)          │  ← HTTP, WebSocket
├─────────────────────────────────────────────┤
│           Application Layer (Services)        │  ← Use Cases, DTOs
├─────────────────────────────────────────────┤
│             Domain Layer (Models)             │  ← Entities, Business Logic
├─────────────────────────────────────────────┤
│         Infrastructure Layer                  │  ← DB, Celery, Cache, External APIs
└─────────────────────────────────────────────┘
```

### Dependency Rule
> Inner layers know NOTHING about outer layers. Domain never imports from Infrastructure.

---

## Module Structure

```
src/
├── apps/
│   ├── tables/          # Table lifecycle management
│   ├── reservations/    # Booking & reminders
│   ├── orders/          # Order management
│   ├── kitchen/         # Kitchen queue & routing
│   ├── menu/            # Menu items, combos, customisation
│   ├── billing/         # POS, tax, split bills
│   └── staff/           # Roles & permissions
├── core/
│   ├── patterns/        # Design pattern base classes
│   └── utils/           # Shared utilities
└── infrastructure/
    ├── celery/          # Async tasks
    └── db/              # Database config
```

Each module follows the same internal structure:
```
apps/<module>/
├── models.py       # Domain entities
├── services.py     # Application logic (use cases)
├── api.py          # FastAPI/DRF endpoints
├── schemas.py      # Pydantic DTOs
├── tasks.py        # Celery async tasks
└── tests/
```

---

## Design Patterns (6 Patterns)

### 1. 🎯 Command Pattern
**Module:** `kitchen`
**Problem:** Kitchen actions (Prepare, Cancel, Expedite) must be undoable and replayable.
**Solution:** Each action is encapsulated as a Command object with `execute()` and `undo()` methods.

```python
# core/patterns/command.py
class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...
    @abstractmethod
    def undo(self) -> None: ...

class KitchenQueue:
    """Invoker — stores and executes commands"""
    def __init__(self):
        self._history: list[Command] = []

    def execute(self, command: Command) -> None:
        command.execute()
        self._history.append(command)

    def undo_last(self) -> None:
        if self._history:
            self._history.pop().undo()
```

---

### 2. 👁️ Observer Pattern
**Module:** `orders`
**Problem:** When order status changes, multiple subsystems (Waiter, Kitchen, Manager) must be notified automatically.
**Solution:** Order is the Subject; Waiter/Kitchen/Manager are Observers.

```python
# core/patterns/observer.py
class Observer(ABC):
    @abstractmethod
    def update(self, event: str, data: dict) -> None: ...

class Subject:
    def __init__(self):
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def notify(self, event: str, data: dict) -> None:
        for observer in self._observers:
            observer.update(event, data)
```

---

### 3. 💰 Strategy Pattern
**Module:** `billing`
**Problem:** Pricing must switch at runtime — Happy Hour, Loyalty Card, Group Discount.
**Solution:** PricingStrategy interface with interchangeable implementations.

```python
# core/patterns/strategy.py
class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, subtotal: Decimal) -> Decimal: ...

class HappyHourPricing(PricingStrategy):
    def calculate(self, subtotal: Decimal) -> Decimal:
        return subtotal * Decimal("0.80")   # 20% off

class LoyaltyCardPricing(PricingStrategy):
    def calculate(self, subtotal: Decimal) -> Decimal:
        return subtotal * Decimal("0.90")   # 10% off
```

---

### 4. 🏗️ Factory Method Pattern
**Module:** `menu`
**Problem:** Creating Starter, MainCourse, Dessert, Beverage objects requires different logic per type.
**Solution:** MenuItemFactory delegates creation to subclass factories.

```python
# core/patterns/factory.py
class MenuItemFactory(ABC):
    @abstractmethod
    def create_item(self, data: dict) -> MenuItem: ...

class StarterFactory(MenuItemFactory):
    def create_item(self, data: dict) -> Starter:
        return Starter(**data)
```

---

### 5. 🎨 Decorator Pattern
**Module:** `menu`
**Problem:** Customers add allergen flags, special prep notes, side substitutions to any dish.
**Solution:** Wrap MenuItems dynamically without changing their class.

```python
# core/patterns/decorator.py
class MenuItemDecorator(MenuItem):
    def __init__(self, component: MenuItem):
        self._component = component

    def get_price(self) -> Decimal:
        return self._component.get_price()

class AllergenFlagDecorator(MenuItemDecorator):
    def get_price(self) -> Decimal:
        return self._component.get_price()  # no price change, adds metadata
```

---

### 6. 🔒 Singleton Pattern
**Module:** `orders`
**Problem:** One global Order History Log must exist across all subsystems.
**Solution:** Thread-safe Singleton using metaclass.

```python
# core/patterns/singleton.py
class SingletonMeta(type):
    _instances: dict = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class OrderHistoryLog(metaclass=SingletonMeta):
    def __init__(self):
        self._records: list[OrderRecord] = []

    def append(self, record: OrderRecord) -> None:
        self._records.append(record)

    def __iter__(self):
        return iter(self._records)
```

---

## Async Tasks (Celery)

| Task | Module | Trigger |
|------|--------|---------|
| `send_reservation_reminder` | reservations | 2h before booking |
| `notify_kitchen_on_order` | kitchen | Order confirmed |
| `generate_end_of_night_report` | billing | Scheduled daily 23:59 |
| `broadcast_order_status` | orders | Status change event |

---

## Microservices Readiness

Each Django app is designed to be extracted into its own service:
- Independent models with no cross-app ForeignKeys (use UUIDs as references)
- Communication via events (Celery/Redis) not direct function calls
- Each app has its own API router, mountable independently

To extract `kitchen` as a microservice:
```bash
cp -r src/apps/kitchen kitchen-service/
# Update EVENT_BUS_URL in .env
```
