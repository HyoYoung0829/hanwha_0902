from fastapi import FastAPI, HTTPException

app = FastAPI()

# 응답에 사용할 HTTP 상태코드를 선언할 수도 있다.
# | 범위    | 의미         |
# | ----- | ---------- |
# | `1xx` | 정보         |
# | `2xx` | 성공         |
# | `3xx` | 리다이렉션      |
# | `4xx` | 클라이언트 쪽 오류 |
# | `5xx` | 서버 쪽 오류    |
# 정해진건 아니고 관례임. 물론 임의로 따로 지정할 수 있음


@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}


# fastapi는 편의 변수를 제공하기 때문에 코드를 외우기보다 편의 변수를 사용하는 법을 길러보자.
@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}


# 클라이언트에  오류가 포함된 HTTP 응답을 반환하려면 HTTPException을 사용한다.

items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        # item_id에 해당하는 데이터가 없으면, 지금 함수 실행을 중단하고 404 Not Found 에러를 클라이언트에게 보내라.
        # HTTPException는 일반적인 반환값이 아니라 예외(Exception)이기 때문에 "return"을 사용하지 않는다.
        # raise는 중간 함수 어디서든 요청 처리를 중단할 수 있기 때문이다.
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
