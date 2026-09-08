# 응답 모델
# 즉 서버가 클라이언트에게 어떤 형태의 JSON을 보내줄지를 연습하는 예제


from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


# "->" 이 표시가 응답의 타입을 지정하는 문법.
# Item 모델의 타입을 따른다~ 라는 소리임.
@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item


# 마찬가지로 리스트의 각 요소에 지정도 가능
@app.get("/items/")
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]


# "->" 이것도 가능하지만 "response_model"로 지정해주는것도 가능함.
# 둘다 동시에 사용하면 fastapi는 "response_model"을 우선시함.
# 함수가 정말 Item을 반환한다면 "->" 쪽이 좋고, IDE의 타입 검사도 잘 받을 수 있음.
# 함수 내부에서는 dict, ORM 객체, DB 객체 등 다른 형태를 반환하지만, 외부 API 응답은 Item으로 제한하고 싶을 때는 "response_model"
@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item


@app.get("/items/", response_model=list[Item])
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]


# exclude_unset
# exclude_include
# exclude_exclude
# 응답도 출력 형식을 조정할 수 있다.
# 이런 옵션을 사용하는것도 좋지만 가능하면 별도의 모델을 만드는것을 권장한다.

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]
