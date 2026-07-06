# BitePlate — UML Diagrams

> All diagrams use PlantUML syntax. Render at https://plantuml.com/plantuml or VS Code PlantUML extension.

---

## Diagram 1: UML Class Diagram — `orders` + `menu` Modules

Demonstrates: **Encapsulation**, **Inheritance**, **Polymorphism**, **Abstraction**, **Composition**, **Aggregation**, **Dependency**, **Realisation**, **Generalisation**

```plantuml
@startuml BitePlate_ClassDiagram

skinparam classAttributeIconSize 0
skinparam classFontStyle Bold
skinparam backgroundColor #FAFAFA
skinparam ArrowColor #555555

' ─────────────────────────────────────────
'  ABSTRACT BASE — Abstraction
' ─────────────────────────────────────────
abstract class MenuItem {
  # id: UUID
  # name: str
  # base_price: Decimal
  # is_available: bool
  + {abstract} get_price(): Decimal
  + {abstract} get_display_name(): str
  + get_category(): str
}

' ─────────────────────────────────────────
'  INTERFACES — Realisation
' ─────────────────────────────────────────
interface Priceable {
  + {abstract} calculate_total(): Decimal
}

interface Auditable {
  + {abstract} get_audit_entry(): dict
}

interface Notifiable {
  + {abstract} notify(event: str, data: dict): None
}

' ─────────────────────────────────────────
'  INHERITANCE (Generalisation) — Polymorphism via get_price()
' ─────────────────────────────────────────
class Starter {
  - prep_time_seconds: int
  + get_price(): Decimal
  + get_display_name(): str
}

class MainCourse {
  - cooking_station: str
  + get_price(): Decimal
  + get_display_name(): str
}

class Dessert {
  - requires_fridge: bool
  + get_price(): Decimal
  + get_display_name(): str
}

class Beverage {
  - is_alcoholic: bool
  - volume_ml: int
  + get_price(): Decimal
  + get_display_name(): str
}

MenuItem <|-- Starter       : generalisation
MenuItem <|-- MainCourse    : generalisation
MenuItem <|-- Dessert       : generalisation
MenuItem <|-- Beverage      : generalisation

' ─────────────────────────────────────────
'  DECORATOR PATTERN — dynamic customisation
' ─────────────────────────────────────────
abstract class MenuItemDecorator {
  # _component: MenuItem
  + get_price(): Decimal
  + get_display_name(): str
}

class AllergenFlagDecorator {
  - allergen: str
  + get_price(): Decimal
  + get_display_name(): str
}

class ExtraIngredientDecorator {
  - ingredient_name: str
  - extra_cost: Decimal
  + get_price(): Decimal
  + get_display_name(): str
}

MenuItem <|-- MenuItemDecorator       : generalisation
MenuItemDecorator <|-- AllergenFlagDecorator
MenuItemDecorator <|-- ExtraIngredientDecorator
MenuItemDecorator o-- MenuItem        : wraps (aggregation)

' ─────────────────────────────────────────
'  COMPOSITE PATTERN — Set Meals
' ─────────────────────────────────────────
class ComboMeal {
  - name: str
  - discount_pct: Decimal
  - items: list<MenuItem>
  + add_item(item: MenuItem): None
  + get_price(): Decimal
  + get_display_name(): str
}

MenuItem <|-- ComboMeal               : generalisation
ComboMeal o-- MenuItem                : contains 1..* (aggregation)

' ─────────────────────────────────────────
'  ORDER DOMAIN
' ─────────────────────────────────────────
class OrderItem {
  - id: UUID
  - quantity: int
  - special_notes: str
  + get_line_total(): Decimal
}

class Order {
  - id: UUID
  - table_id: UUID
  - staff_id: UUID
  - status: OrderStatus
  - created_at: datetime
  - items: list<OrderItem>
  + add_item(item: OrderItem): None
  + remove_item(item_id: UUID): None
  + get_subtotal(): Decimal
  + confirm(): None
  + cancel(): None
}

class OrderStatus {
  <<enumeration>>
  DRAFT
  CONFIRMED
  IN_KITCHEN
  SERVED
  CANCELLED
}

' ─────────────────────────────────────────
'  SINGLETON — Order History Log
' ─────────────────────────────────────────
class OrderHistoryLog {
  - {static} _instance: OrderHistoryLog
  - _records: list<OrderRecord>
  - {static} _lock: Lock
  - OrderHistoryLog()
  + {static} get_instance(): OrderHistoryLog
  + append(record: OrderRecord): None
  + get_by_table(table_id: UUID): list<OrderRecord>
  + get_by_date_range(start: date, end: date): list<OrderRecord>
  + __iter__(): Iterator
}

class OrderRecord {
  + order_id: UUID
  + table_number: int
  + staff_id: UUID
  + total: Decimal
  + timestamp: datetime
  + get_audit_entry(): dict
}

' ─────────────────────────────────────────
'  RELATIONSHIPS
' ─────────────────────────────────────────
Order "1" *-- "1..*" OrderItem       : composition
OrderItem --> MenuItem                : depends on
Order --> OrderStatus                 : uses
Order ..|> Auditable                  : realises
Order ..|> Priceable                  : realises
OrderHistoryLog "1" o-- "0..*" OrderRecord : aggregation
OrderRecord ..|> Auditable            : realises

note top of OrderHistoryLog
  **Singleton Pattern**
  Only one instance exists globally.
  Thread-safe via Lock.
end note

note right of MenuItemDecorator
  **Decorator Pattern**
  Adds allergens / extras
  at runtime without
  modifying MenuItem subclasses.
end note

note bottom of ComboMeal
  **Composite Pattern**
  ComboMeal IS-A MenuItem,
  so it can contain other
  MenuItems uniformly.
end note

@enduml
```

---

## Diagram 2: Use Case Diagram

```plantuml
@startuml BitePlate_UseCaseDiagram

skinparam actorStyle awesome
skinparam backgroundColor #FAFAFA
skinparam ArrowColor #444

left to right direction

actor Customer as C
actor Waiter as W
actor Chef as CH
actor Cashier as CA
actor Manager as M
actor "Celery Scheduler" as CS

rectangle BitePlate {

  ' ── Customer
  usecase "Make Reservation" as UC1
  usecase "Customise Dish" as UC2
  usecase "Split Bill Request" as UC3

  ' ── Waiter
  usecase "Seat Customer" as UC4
  usecase "Take Order" as UC5
  usecase "Modify Order\n(before kitchen)" as UC6
  usecase "Send to Kitchen" as UC7
  usecase "Receive Order Ready\nNotification" as UC8

  ' ── Chef
  usecase "View Kitchen Queue" as UC9
  usecase "Prepare / Cancel Item" as UC10
  usecase "Undo Last Action" as UC11
  usecase "Reprioritise Queue" as UC12

  ' ── Cashier
  usecase "Generate Bill" as UC13
  usecase "Apply Discount" as UC14
  usecase "Process Payment" as UC15
  usecase "Close Table" as UC16

  ' ── Manager
  usecase "View Order History" as UC17
  usecase "Run End-of-Night Report" as UC18
  usecase "Manage Staff Roles" as UC19
  usecase "Override Any Order" as UC20

  ' ── Scheduler
  usecase "Send Reservation Reminder" as UC21
  usecase "Auto-switch Pricing Mode" as UC22

  ' ── Relationships
  C --> UC1
  C --> UC2
  C --> UC3

  W --> UC4
  W --> UC5
  W --> UC6
  W --> UC7
  W --> UC8

  CH --> UC9
  CH --> UC10
  CH --> UC11
  CH --> UC12

  CA --> UC13
  CA --> UC14
  CA --> UC15
  CA --> UC16

  M --> UC17
  M --> UC18
  M --> UC19
  M --> UC20

  CS --> UC21
  CS --> UC22

  ' ── Include / Extend
  UC5 .> UC2 : <<include>>
  UC13 .> UC14 : <<extend>>
  UC15 .> UC16 : <<include>>
  UC7 .> UC8 : <<include>>
  UC10 .> UC11 : <<extend>>
}

@enduml
```

---

## Diagram 3: Activity Diagrams (3 Scenarios)

### Scenario A — Full Order Lifecycle (Customer → Bill Settled)

```plantuml
@startuml BitePlate_Activity_OrderLifecycle

skinparam backgroundColor #FAFAFA
skinparam ArrowColor #444

|Customer|
|Waiter|
|System|
|Kitchen|
|Cashier|

title Scenario A: Full Order Lifecycle

|Customer|
start
:Arrives at restaurant;

|Waiter|
:Checks available tables;
:Assigns table (State: RESERVED → OCCUPIED);

|Customer|
:Reviews menu;
:Requests order with customisations;

|Waiter|
:Creates Order (DRAFT);
:Adds OrderItems + Decorator extras;

if (Customer modifies order?) then (yes)
  :Update OrderItems;
endif

:Confirms Order (DRAFT → CONFIRMED);

|System|
:Observer notifies Kitchen;
:Command pushed to KitchenQueue;
:OrderHistoryLog.append() — Singleton;

|Kitchen|
:Chef executes PrepareOrderCommand;

if (Item unavailable?) then (yes)
  :Execute CancelOrderCommand;
  :Notify Waiter via Observer;
  |Waiter|
  :Inform Customer, take replacement order;
  |Kitchen|
else (no)
endif

:Mark items READY;

|System|
:Observer notifies Waiter;

|Waiter|
:Serve dishes to table;
:Update Order status → SERVED;

|Customer|
:Request bill;

|Cashier|
:Facade.generate_bill();
:Apply PricingStrategy (Standard/HappyHour/Loyalty);
:Calculate tax, handle tip;

if (Split bill?) then (yes)
  :Divide bill between guests;
endif

:Process payment;
:Table status → AWAITING_BILL → CLEARED;

|System|
:Celery task: archive session;
stop

@enduml
```

### Scenario B — Reservation & Reminder Pipeline

```plantuml
@startuml BitePlate_Activity_Reservation

skinparam backgroundColor #FAFAFA

|Customer|
|System|
|"Celery Scheduler"|
|Manager|
|Waiter|

title Scenario B: Reservation & Reminder Pipeline

|Customer|
start
:Request table reservation;

|System|
:Validate time slot availability;

if (Slot available?) then (no)
  :Return error — suggest alternatives;
  stop
endif

:Create Reservation (Table: RESERVED);
:Trigger Observer → notify Manager Dashboard;
:Celery: schedule reminder task (T - 2h);

|Manager|
:Calendar view updated (Observer);

|"Celery Scheduler"|
:T - 2h: send_reservation_reminder fires;
:SMS notification to customer;

|System|
:Log reminder sent;

|Waiter|
:Customer arrives — verify reservation;
:Table RESERVED → OCCUPIED;

stop

@enduml
```

### Scenario C — End-of-Night Report (Iterator + Singleton)

```plantuml
@startuml BitePlate_Activity_NightReport

skinparam backgroundColor #FAFAFA

|Manager|
|System|
|"OrderHistoryLog (Singleton)"|
|"Celery Task"|

title Scenario C: End-of-Night Report

|"Celery Task"|
start
:Scheduled trigger at 23:59;

|System|
:Call OrderHistoryLog.get_instance();

|"OrderHistoryLog (Singleton)"|
:Return single global instance;

|System|
:Iterate records via __iter__ (Iterator Pattern);

repeat
  :Read OrderRecord;
  :Accumulate revenue by category;
  :Count orders per staff member;
  :Flag cancelled-after-prep records (waste);
repeat while (more records?) is (yes)
-> no;

|Manager|
:Display report:
- Total revenue (food vs drinks)
- Top 3 waitstaff by covers
- Waste metric (cancelled after prep)
- Peak hour analysis;

:Export to PDF / CSV;
stop

@enduml
```

---

## Diagram 4: Sequence Diagram — Order Placement Flow

```plantuml
@startuml BitePlate_SequenceDiagram

skinparam backgroundColor #FAFAFA
skinparam SequenceArrowThickness 1.5
skinparam ParticipantFontStyle Bold

title Order Placement: Waiter → Kitchen → Observer Notifications

actor Waiter as W
participant "OrderAPI\n(FastAPI)" as API
participant "OrderService" as OS
participant "Order\n(Subject)" as O
participant "KitchenQueue\n(Invoker)" as KQ
participant "PrepareOrderCommand" as CMD
participant "Chef\n(Receiver)" as CH
participant "WaiterNotifier\n(Observer)" as WN
participant "ManagerDashboard\n(Observer)" as MD
participant "OrderHistoryLog\n(Singleton)" as OHL
participant "CeleryBroker\n(Redis)" as CB

W -> API : POST /orders {table_id, items}
activate API

API -> OS : create_order(table_id, items)
activate OS

OS -> O : Order(status=DRAFT)
activate O

OS -> O : confirm()
O -> O : status = CONFIRMED
O -> WN : notify("ORDER_CONFIRMED", data)
O -> MD : notify("ORDER_CONFIRMED", data)

OS -> OHL : get_instance()
OHL --> OS : singleton_instance
OS -> OHL : append(OrderRecord(...))

OS -> CB : send_task("notify_kitchen_on_order", order_id)
activate CB
CB --> OS : task_id
deactivate CB

note over CB
  Celery picks up task asynchronously
end note

CB -> KQ : [async] execute command
activate KQ
KQ -> CMD : PrepareOrderCommand(order)
activate CMD
CMD -> CH : prepare(order_items)
activate CH
CH --> CMD : ack
deactivate CH
CMD --> KQ : done
deactivate CMD

KQ -> O : update status → IN_KITCHEN
O -> WN : notify("ORDER_IN_KITCHEN", data)
deactivate KQ

OS --> API : OrderDTO(id, status)
deactivate OS
deactivate O

API --> W : 201 Created {order_id, status}
deactivate API

== Later: Item ready ==

CH -> O : mark_ready(item_id)
activate O
O -> WN : notify("ITEM_READY", {table: 5, item: "Pasta"})
WN --> W : WebSocket push: "Table 5 pasta is ready"
deactivate O

@enduml
```

---

## Rendering Instructions

| Tool | How |
|------|-----|
| **VS Code** | Install "PlantUML" extension → right-click → Preview |
| **Online** | Go to https://www.plantuml.com/plantuml/uml → paste code |
| **CLI** | `java -jar plantuml.jar diagrams.md` |
| **Docker** | `docker run -p 8080:8080 plantuml/plantuml-server` |
