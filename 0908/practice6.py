from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# 베이스 모델을 사용하면 기본적인 타입 검증은 됨.
# 그러나 바디 속성 내부에 디테일한 검증을 원한다면 Field()를 사용할 수 있음.
# 즉 클래스 내부에서는 field()를 사용해서 검증
# 엔드포인트 함수에서는 body()로 검증.

# Body()는 FastAPI가 요청에서 이 파라미터를 어떻게 받을지를 다루고,
# Field()는 Pydantic 모델 안의 속성을 어떻게 검증할지를 다룸.


class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results
