# fasstapi 임포트
from fastapi import FastAPI

# 인스턴스 생성
app = FastAPI()


# get api 생성
# 엔드포인트는 루트
@app.get("/")
# async - 비동기
# root() - 함수 이름
async def root():
    return {"message": "Hello World"}


# 경로 매개변수
# "{item_id}"와 같이 url에 매개변수를 받을 수 있다.
@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}


# 경로 매개변수의 타입을 지정할 수 있음.
# URL에서 "123"처럼 문자열 형태로 들어와도 int 타입으로 변환 가능하면 123으로 변환해줌.
# int로 변환할 수 없는 값이 들어오면 함수는 실행되지 않고 422 에러를 반환.
# 실수도 422에러를 반환. 소수점을 알아서 버려주지 않음.
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
