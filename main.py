from contextlib import asynccontextmanager
from typing import List
from core.models import Base, db_helper
import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError
from items_views import router as items_router
from users.views import router as users_router, fake_trades
from  api_v1 import router as router_v1
from core.settings import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(title="Trading App", lifespan=lifespan)
app.include_router(router=router_v1,prefix=settings.api_v1_prefix)
app.include_router(items_router)
app.include_router(users_router)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


@app.get("/")
def hello():
    return {"message": "Hello world"}


@app.get("/hello/")
def hello(name: str):
    name = name.strip().title()
    return {"message": f"Hello {name}"}


@app.post("/calc/add/")
def add(a: int, b: int):
    return {
        "a": a,
        "b": b,
        "result": a + b,
    }


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str
    side: str
    price: float = Field(ge=0)
    amount: float


@app.post("/trades")
def add_trades(trade: List[Trade]):
    fake_trades.extend(trade)
    return {"status": 200, "data": fake_trades}


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
    # hello()
    # get_users(1)
    # change_name_users(1, 'Bob')
    # add_trades('trade')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/ и т.д....
