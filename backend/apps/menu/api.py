from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from .schemas import MenuItemCreate, MenuItemResponse, ComboMealCreate, CustomisationRequest
from .services import MenuService

router = APIRouter(prefix="/menu", tags=["Menu"])
_service = MenuService()


@router.get("/items", response_model=list[MenuItemResponse])
def list_items():
    """List all available menu items."""
    items = _service.list_available()
    return [
        MenuItemResponse(
            id=i.id,
            name=i.get_display_name(),
            description=i.description,
            base_price=i.get_price(),
            category=i.category,
            is_available=i.is_available,
            allergens=i.get_allergens(),
        )
        for i in items
    ]


@router.post("/items", response_model=MenuItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(body: MenuItemCreate):
    """Create a new menu item via Factory Method."""
    try:
        item = _service.create_menu_item(body)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return MenuItemResponse(
        id=item.id,
        name=item.name,
        description=item.description,
        base_price=item.base_price,
        category=item.category,
        is_available=item.is_available,
        allergens=[],
    )


@router.post("/items/{item_id}/customise")
def customise_item(item_id: UUID, body: CustomisationRequest):
    """
    Apply Decorator layers to a menu item.
    Returns decorated name and price — does not persist.
    """
    body.menu_item_id = item_id
    try:
        component = _service.customise_item(body)
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return {
        "display_name": component.get_display_name(),
        "final_price": float(component.get_price()),
        "allergens": component.get_allergens(),
    }


@router.post("/combos", status_code=status.HTTP_201_CREATED)
def create_combo(body: ComboMealCreate):
    """Create a combo meal (Composite Pattern)."""
    combo = _service.create_combo(body)
    return {
        "id": combo.id,
        "name": combo.get_display_name(),
        "final_price": float(combo.get_price()),
    }


@router.patch("/items/{item_id}/availability")
def toggle_availability(item_id: UUID):
    item = _service.toggle_availability(item_id)
    return {"id": item.id, "is_available": item.is_available}
