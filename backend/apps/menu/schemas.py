from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Optional, List


class MenuItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    base_price: Decimal = Field(..., gt=0)
    category: str  # starter | main | dessert | beverage
    prep_time_seconds: int = 600
    cooking_station: str = ""


class MenuItemResponse(BaseModel):
    id: UUID
    name: str
    description: str
    base_price: Decimal
    category: str
    is_available: bool
    allergens: List[str] = []

    class Config:
        from_attributes = True


class ComboMealCreate(BaseModel):
    name: str
    description: str = ""
    discount_pct: Decimal = Decimal("10.00")
    item_ids: List[UUID]


class AllergenCreate(BaseModel):
    name: str
    menu_item_id: UUID


class CustomisationRequest(BaseModel):
    """Request to customise a menu item with decorators."""
    menu_item_id: UUID
    allergen_flags: List[str] = []
    extra_ingredients: List[dict] = []   # [{ingredient, extra_cost}]
    special_note: Optional[str] = None
