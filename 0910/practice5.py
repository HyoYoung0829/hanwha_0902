# JSON Lines 스트리밍
# SSE와 비슷해보이지만 목적이 조금 다음.
# 핵심은 “JSON 데이터를 한 줄씩 계속 보내는 스트리밍 방식” 이다.

# 보통은 이런 JSON의 전체 배열이 완성되어야 클라이언트가 받기 시작함
[
    {"name": "Plumbus"},
    {"name": "Portal Gun"},
    {"name": "Meeseeks Box"},
]

# JSON Lines 스트리밍은 한줄 씩 보내는것을 의미함.
# [] 도 없고 , 도 없다. 저스트 줄바꿈으로만 구분하고
# 컨텐츠 타입도 application/jsonl 이거임.

# 핵심은 첫번째 객체가 완료가 되면 바로 전송한다. 이 점에서 스트리밍이라는거임.

from collections.abc import AsyncIterable

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None


items = [
    Item(name="Plumbus", description="A multi-purpose household device."),
    Item(name="Portal Gun", description="A portal opening device."),
    Item(name="Meeseeks Box", description="A box that summons a Meeseeks."),
]


@app.get("/items/stream")
# Item을 하나만 반환하는 게 아니라 비동기적으로 여러 개 계속 내보낼 수 있는 함수라는 뜻.
async def stream_items() -> AsyncIterable[Item]:
    for item in items:
        yield item


# SSE이랑 무슨 차이인가?
# SSE는 "이벤트 프로토콜"
# JSON Lines는 "JSON 객체를 줄 단위로 흘려보내는 데이터 형식"

# 즉 구조화된 데이터를 그냥 계속 보내고 싶으면 JSON Lines가 더 단순.
# 이벤트 종류나 재연결 같은 SSE 기능이 필요하면 SSE가 더 적합.

# 일반 def도 가능


# 검색 결과 1000개
# 로그 데이터
# LLM이 생성하는 구조화된 객체
# Agent 실행 결과 객체
# 를 계속 내려보내고 싶다:

# → JSON Lines


# message 이벤트
# progress 이벤트
# done 이벤트
# 연결 재시도
# Last-Event-ID
# 같은 이벤트 의미가 중요하다:

# → SSE


# 일반 JSON
# → 모든 결과를 모아서 한 번에

# JSON Lines
# → JSON 하나 완성될 때마다 바로 전송

# SSE
# → JSON보다 더 큰 개념인 "이벤트"를 스트리밍


# SSE는 data라는 필드 안에 json을 담아서 보냄
# data: {"name": "Plumbus", "description": "..."}
# data: {"name": "Portal Gun", "description": "..."}

# JSON Lines은 진짜로 순수 JSON 객체를 줄바꿈으로 구분해서 보내는 방식.
# {"name": "Plumbus", "description": "..."}
# {"name": "Portal Gun", "description": "..."}
