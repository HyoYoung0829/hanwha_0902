# 테스트
# api가 많아지면 하나씩 스웨거에서 검사하는게 일이 됨.
# 따라서 서버를 띄우지 않고 더욱 빠르게 테스트하는 방법을 소개함.
# FastAPI에 테스트용 HTTP 요청을 보내는 도구 = "TestClient"
# 테스트 함수들을 찾아서 실행하고, 성공/실패를 판단해서 결과를 보여주는 테스트 실행기 = "pytest"
# 추후 pytest 이것도 배워서 테스트 환경을 구성하는게 좋아보임.


# TestClient
# ≈ fetch / axios 역할

# pytest
# ≈ Vitest / Jest 역할

from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


# 실제 브라우저나 프론트엔드 대신 테스트 코드가 FastAPI에 요청을 보낼 수 있음.
# 이전) 브라우저 → FastAPI / 현재) TestClient → FastAPI
# Jest랑 비슷한데 실제 FastAPI 라우팅 로직을 그대로 테스트한다는 점이 포인트.
client = TestClient(app)


def test_read_main():
    # 브라우저 요청처럼 보면 됨.
    response = client.get("/")

    # 여기가 진짜 테스트 부분.
    # 뜻 : 응답 status code가 200이어야 한다.
    # 뜻 : 응답 JSON이 정확히 이 값이어야 한다.
    # assert는 조건이 False면 테스트를 실패시킴.
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
