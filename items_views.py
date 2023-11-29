from typing import Annotated

from fastapi import APIRouter, Path

router = APIRouter(prefix="/items",tags=['items'])


@router.get("/")
def list_items():
    return {
        "items1",
        "items2",
        "items3",
    }


@router.get("/{item_id}/")
def get_items_by_id(item_id: Annotated[int, Path(ge=1, lt=1_000_000)]):
    return {
        "items": {
            "id": item_id,
        },
    }
