# 하위 의존성
# 의존성 함수를 중첩해서 사용할 수 있음.
# 해당 순서나 처리는 fastapi가 전부 해줌

from typing import Annotated

from fastapi import Cookie, Depends, FastAPI

app = FastAPI()


def query_extractor(q: str | None = None):
    return q


def query_or_cookie_extractor(
    # 여기서 "query_extractor"를 다시 넘겨줌
    q: Annotated[str, Depends(query_extractor)],
    last_query: Annotated[str | None, Cookie()] = None,
):
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(
    # fastapi가 쭉쭉 들어가서 필요한 함수들을 전부 실행해서 해당 api에 필요한 준비를 다 해줌
    query_or_default: Annotated[str, Depends(query_or_cookie_extractor)],
):
    return {"q_or_cookie": query_or_default}


# fastapi는 api 요청당 의존성 함수를 한번만 실행하는것으로 정해둠.
# 만약 한 api에서 같은 의존성 함수를 여러번 호출하면 캐싱된 결과 값을 재사용하는데
# 여러번 함수를 호출해야 한다면 "use_cache=False" 옵션을 사용해서 매번 실행할 수 있게 할 수 있다.
async def needy_dependency(
    fresh_value: Annotated[str, Depends(get_value, use_cache=False)],
):
    return {"fresh_value": fresh_value}
