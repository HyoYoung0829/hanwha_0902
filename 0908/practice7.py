from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()

# 해당 예제는 중첩 모델을 설명하는 예제.
# 데이터는
# {
#     "name": "Foo",
#     "price": 42,
#     "image": {"url": "http://example.com/foo.jpg", "name": "상품 이미지"},
# }
# 이런식으로 객체 안에 객체가 들어올 수 있음.
# 이 경우 새로운 클래스를 만들어서 "image에는 아무 dict나 들어오는 게 아니라 Image 모델 구조에 맞는 객체가 들어와야 한다!" 라고 선언 할 수 있음.
# 즉 이것이 중첩 모델임.


class Image(BaseModel):
    # 보통 url은 문자열이라서 타입을 str로 생각하는 경우가 많은데
    # 더 강한 검증을 위해서는 pydantic의 "HttpUrl"를 사용하면
    # 그냥 문자열이 아니라 실제 HTTP/HTTPS URL 형태인지 확인하게 된다.
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    # Image 모델에 맞는 데이터를 받아야 함.
    image: Image | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


# body 자체가 리스트가 들어올 수도 있음.
class Image(BaseModel):
    url: HttpUrl
    name: str


@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return images
