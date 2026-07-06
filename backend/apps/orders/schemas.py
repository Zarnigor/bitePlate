from uuid import UUID
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    menu_item_id: UUID
    name: str
    unit_price: Decimal
    quantity: int = 1
    special_notes: str = ""


class OrderCreate(BaseModel):
    table_id: UUID
    staff_id: UUID
    items: List[OrderItemCreate]


class OrderItemResponse(BaseModel):
    id: UUID
    menu_item_name: str
    unit_price: Decimal
    quantity: int
    line_total: Decimal
    special_notes: str

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: UUID
    table_id: UUID
    staff_id: UUID
    status: str
    subtotal: Decimal
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True
