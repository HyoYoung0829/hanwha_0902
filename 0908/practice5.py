from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


# 다중 모델을 선언하여 동시에 검사 할 수 있음.
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results


# body 안에 들어오는 데이터를 별개의 모델로 각각 검증 할 수 있다.
# 또한 "Body()" 통해 특정 값을 "body"에서 찾아라~ 라고 명시해 줄 수 있음.
# 만약 "Body()"를 안붙이면 fastapi는 기본적으로 쿼리 파라미터라고 판단함
@app.put("/items/{item_id}")
async def update_item(
    item_id: int, item: Item, user: User, importance: Annotated[int, Body()]
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results
