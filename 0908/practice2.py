# fasstapi 임포트
from fastapi import FastAPI

# 인스턴스 생성
app = FastAPI()


# api 선언 순서 문제
# 만약 /users/me 요청이 오면 응답으로 "the current user" 이게 반환 됨.
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


# -----------------------------------------------------


# 만약 이렇게 api 선언 순서가 바뀐 다음
# /users/me 요청이 오면 응답으로 "user_id": me 가 반환 됨.
@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


# 따라서 api 선언의 순서도 고려하여 코드를 작성해야하며
# 고정 경로를 동적 경로보다 먼저 선언해야 한다.


# 매개변수 여러개
# 여러개의 매개변수를 받을 수 있으며 순서는 상관없다.
# 키 값으로 매칭하기 때문
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
