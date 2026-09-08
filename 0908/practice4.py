from fastapi import FastAPI
from pydantic import BaseModel


# 보통 post 메서드는 pydantic이랑 같이 씀.
# get 메서드는 보통 함수 인자 타입으로 검사하고 body에 감싸진 데이터는 pydantic으로 검사함.
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.post("/items/")
# 데이터를 받는데 Item 클래스를 상속한다.
# Item 클래스는 BaseModel를 상속 받았기 때문에 여기서 검사가 이루어지는듯?
async def create_item(item: Item):
    return item


# 모델 사용하기
# Item 객체에 요소를 추가하기 위해서 dict로 변환 후 요소를 추가한다.
# 클래스의 존재 의미는 "이 구조는 반드시 지켜야한다!" 이기 때문에
# 해당 구조를 바꾸거나 변경하는건 dict로 변환해서 사용하는게 권장됨
@app.post("/items/")
async def create_item(item: Item):
    # Item 객체 -> dict
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# path + query + body 한번에 받기
# fastapi는 한번에 받을 수 있음.
class Item1(BaseModel):
    name: str
    price: float


@app.put("/items/{item_id}")
async def update_item(
    item_id: int, q: str | None = None, item: Item1 = None  # Path  # Query  # Body
):
    return {"item_id": item_id, "q": q, "item": item}
