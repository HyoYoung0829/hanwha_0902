# 의존성
# 해당 api가 실행되기 전에 필요한 공통 작업을 fastapi가 대신 실행하고
# 그 결과를 넣어주는 기능
# ex) "이 API 실행하려면 먼저 이 함수 결과가 필요해"
# 공통 로직, DB 연결, 인증/권한 처리 등에 특히 유용

from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


# 비동기 함수
# 그냥 다른 API들이 공통으로 사용할 함수.
async def common_parameters(
    q: str | None = None,
    skip: int = 0,
    limit: int = 100,
):
    return {
        "q": q,
        "skip": skip,
        "limit": limit,
    }


@app.get("/items/")
# fastapi는 "/items/" 해당 엔드포인트로 요청이 들어오면 read_items를 보게 됨.
# 그러고 나서 “아, read_items를 실행하려면 먼저 common_parameters 결과가 필요하구나”라고 판단.


# 왜 common_parameters() 가 아니고 common_parameters 인가?
# => 당장 실행하는게 아니라 함수자체를 fastapi에게 넘긴다는 의미.


# "commons: Annotated[dict, Depends(common_parameters)]"의 의미.
# => commons는 dict 타입이고, 그 값은 common_parameters dependency의 결과로 받아와.
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


# 이거 왜 쓰나?
# => 코드 중복을 줄일 수 있음 / 함수별 책임을 분리 시킬 수 있음

# 해커톤에서 어떻게 활용할 수 있는가?
# => Agent를 실행하려면 LLM, DB, 사용자 정보 등이 필요하다고 가정해보자.
# => LLM 생성 과정, DB 연결 과정, 사용자 인증 과정을 분리하면
# => api 로직은 Agent 실행 로직에만 집중할 수 있다.
