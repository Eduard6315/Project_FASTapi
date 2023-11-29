from fastapi import APIRouter
from users.schemas import CreateUser, User
from typing import List
from users import crud

router = APIRouter(prefix="/users", tags=["Users"])

fake_users = [
    {"id": 1, "role": "admin", "name": "Ed"},
    {"id": 2, "role": "trade", "name": "Sam"},
]

fake_users2 = [
    {"id": 1, "role": "admin", "name": "Ed"},
    {"id": 2, "role": "trade", "name": "Sam"},
]

fake_trades = [
    {
        "id": 1,
        "user_id": 1,
        "currency": "BTC",
        "side": "buy",
        "price": 123,
        "amount": 2.12,
    },
    {
        "id": 2,
        "user_id": 2,
        "currency": "BTC",
        "side": "sell",
        "price": 126,
        "amount": 2.12,
    },
]


@router.post("/")
def create_user(user: CreateUser):
    return crud.create_user(user_in=user)


@router.get("/{user_id}", response_model=List[User])
def get_users(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]


@router.post("{user_id}")
def change_name_users(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get("id") == user_id, fake_users2))[0]
    current_user["name"] = new_name
    return {"status": 200, "data": current_user}
