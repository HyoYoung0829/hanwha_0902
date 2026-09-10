# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()


# db = {
#     "id": "gydud7300",
#     "password": "1234",
# }


# class User(BaseModel):
#     username: str
#     password: str


# @app.post("/login")
# def login(login_data: User, status=200):
#     if login_data.username == db["id"] and login_data.password == db["password"]:
#         return {"message": "로그인에 성공했습니다!", "username": login_data.username}

#     else:
#         return {"message": "아이디 또는 비밀번호가 틀렸습니다."}


# --------------------------------------------------------------

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class UserInput(BaseModel):
    name: str
    age: int


@app.get("/")
def read_root():
    return {"message": "FastAPI 서버가 정상 동작 중입니다."}


@app.post("/predict")
def process_data(data: UserInput):
    # 비즈니스 로직 및 AI 모델 추론 처리 위치
    is_adult = data.age >= 19
    message = f"안녕하세요 {data.name}님! " + (
        "성인입니다." if is_adult else "미성년자입니다."
    )

    return {"status": "success", "result_message": message, "is_adult": is_adult}
