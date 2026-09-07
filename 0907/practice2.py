from pydantic import BaseModel
from typing import Annotated, Literal
from annotated_types import Gt


class Fruit(BaseModel):
    name: str
    # 값까지 지정해버린 것.
    # 'red' , 'green'으로 제한.
    color: Literal["red", "green"]
    # "Annotated" 기본 타입에 추가적인 메타데이터나 검증 규칙을 붙이는 문법
    # 실수 타입이어야 하고, "0"이상이어야 함.
    weight: Annotated[float, Gt(0)]
    bazam: dict[str, list[tuple[int, bool, float]]]


print(Fruit(name="Apple", color="red", weight=4.2, bazam={"foobar": [(1, True, 0.1)]}))
