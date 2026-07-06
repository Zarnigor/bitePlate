from uuid import UUID
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .models import Table

router = APIRouter(prefix="/tables", tags=["Tables"])


class TableCreate(BaseModel):
    number: int
    capacity: int = 4
    location: str = ""


ACTIONS = {
    "reserve": lambda t: t.reserve(),
    "seat": lambda t: t.seat(),
    "request_bill": lambda t: t.request_bill(),
    "clear": lambda t: t.clear(),
}


@router.get("/")
def list_tables():
    return [
        {"id": t.id, "number": t.number, "capacity": t.capacity, "status": t.status, "location": t.location}
        for t in Table.objects.all()
    ]


@router.post("/", status_code=201)
def create_table(body: TableCreate):
    table = Table.objects.create(**body.model_dump())
    return {"id": table.id, "number": table.number, "status": table.status}


@router.post("/{table_id}/{action}")
def perform_action(table_id: UUID, action: str):
    """
    Unified state transition endpoint.
    action: reserve | seat | request_bill | clear
    """
    if action not in ACTIONS:
        raise HTTPException(status_code=400, detail=f"Unknown action: {action}")
    try:
        table = Table.objects.get(id=table_id)
        ACTIONS[action](table)
    except Table.DoesNotExist:
        raise HTTPException(status_code=404, detail="Table not found")
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return {"table_id": str(table.id), "status": table.status}
