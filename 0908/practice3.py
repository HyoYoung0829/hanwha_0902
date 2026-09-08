# fasstapi 임포트
from fastapi import FastAPI

# 인스턴스 생성
app = FastAPI()


# 보통 경로 매개변수는 "/"를 받지 못함.
# 그러나 만약 해당 매개변수가 path라면 ":path"를 붙여 /까지 포함해서 받을 수 있다.
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


# 쿼리 매개변수
# 쿼리는 URL에서 ? 후에 나오고 &으로 구분되는 키-값 쌍의 집합.
# ex) http://127.0.0.1:8000/items/?skip=0&limit=10
# 기본적으로 쿼리 매개변수는 url의 일부임으로 문자열임.
# 그러나 타입을 지정해주면 자동으로 검사 및 변환을 진행함.
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
# skip의 자료형은 int고 기본 값은 0이다.
# limit의 자료형은 int고 기본 값은 10이다.
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


# boolean 자료형
# 쿼리 매개변수의 자료형으로 boolean을 사용 할 수 있다.
# 또한 fastapi가 자동으로 유연하게 변환해준다.
# True로 이해하는 표현들
# ?short=true
# ?short=True
# ?short=1
# ?short=yes
# ?short=on


# False로 이해하는 표현들
# ?short=false
# ?short=0
# ?short=no
# ?short=off
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
