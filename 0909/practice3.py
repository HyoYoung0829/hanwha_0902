# 경로처리 데코레이터에서의 의존성


from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()


async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


# "dependencies=[Depends(verify_token)"
# 만약 의존성 함수를 실행해야하긴 하는데 해당 함수가 반환하는 값이 없다면?, 즉 검사 함수 같은 녀석이면
# 위와 같이 작성할 수 있다. 이렇게 되면 함수 실행만 됨.
# 불필요한 매개변수를 만들지 않아도 됨.
# 여러개도 가능.
@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]


# 하위 의존성과의 차이.
# 하위 의존성으로 구조를 짜면 순서가 보장됨
# 데코레이터에 여러개를 넣는 상황은 fastapi가 임의로 실행하기 때문에 순서가 보장되지 않음.
