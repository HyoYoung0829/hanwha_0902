# SSE
# Server-Sent Events
#
# 어디에 쓰이나?
# => 서버가 응답을 한 번에 완성해서 보내는 게 아니라
# => 데이터를 생성되는 순서대로 조금씩 클라이언트에 보내는 방식.
#
# AI 서비스에서는 LLM 응답 스트리밍 같은 곳에 활용할 수 있음.


from collections.abc import AsyncIterable, Iterable
from typing import Annotated

from fastapi import FastAPI, Header
from fastapi.sse import EventSourceResponse, ServerSentEvent
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


# SSE를 스트리밍하려면
# response_class=EventSourceResponse를 지정하고,
# 함수에서 yield로 값을 하나씩 내보낼 수 있음.
#
# yield는 함수를 완전히 종료하지 않고,
# 값을 하나 반환한 뒤 실행 상태를 유지함.
#
# 그래서:
# for item in items:
#     yield item
#
# 첫 번째 item 전송
# → 두 번째 item 전송
# → 세 번째 item 전송
#
# 식으로 데이터를 순차적으로 보낼 수 있음.


@app.get("/items/stream", response_class=EventSourceResponse)
async def sse_items() -> AsyncIterable[Item]:
    for item in items:
        yield item


# 웹소켓과의 차이
#
# WebSocket
# → 클라이언트 ↔ 서버 양방향 통신
#
# SSE
# → 서버 → 클라이언트 단방향 스트리밍
#
# 둘 다 실시간성이 필요한 기능에 활용할 수 있지만
# 통신 방향과 사용 목적이 다름.


# async가 아니어도 SSE 사용 가능.
# 비동기 함수면 AsyncIterable,
# 일반 함수면 Iterable을 반환 타입으로 사용할 수 있음.


@app.get("/items/stream-sync", response_class=EventSourceResponse)
def sse_items_no_async() -> Iterable[Item]:
    for item in items:
        yield item


# SSE는 단순 data뿐 아니라 메타데이터를 함께 보낼 수 있음.
#
# data
# event
# id
# retry
# comment
#
# 이런 값을 직접 지정하고 싶으면 ServerSentEvent 사용.


@app.get("/items/stream-detail", response_class=EventSourceResponse)
async def stream_items_detail() -> AsyncIterable[ServerSentEvent]:

    # comment만 있는 이벤트
    yield ServerSentEvent(comment="stream of item updates")

    for i, item in enumerate(items):
        yield ServerSentEvent(
            data=item,  # 실제 데이터
            event="item_update",  # 이벤트 종류
            id=str(i + 1),  # 이벤트 ID
            retry=5000,  # 재연결 대기 시간(ms)
        )


# ServerSentEvent(data=...)
# → data는 JSON 형태로 직렬화되어 전송될 수 있음.
#
# raw_data
# → JSON 직렬화 없이 문자열 등 raw 데이터를 그대로 보내고 싶을 때 사용.
#
# data와 raw_data는 같은 이벤트에서 동시에 사용하지 않음.


# SSE 연결은 네트워크 문제 등으로 중간에 끊길 수 있음.
# 이때 Last-Event-ID를 이용해서 이어받는 구조를 만들 수 있음.
#
# 클라이언트가:
# Last-Event-ID: 2
#
# 같은 헤더를 보내면
# 서버는 2번 이벤트 다음부터 다시 보내도록 구현할 수 있음.


@app.get("/items/stream-resume", response_class=EventSourceResponse)
async def stream_items_resume(
    last_event_id: Annotated[int | None, Header()] = None,
) -> AsyncIterable[ServerSentEvent]:

    start = last_event_id + 1 if last_event_id is not None else 0

    for i, item in enumerate(items):

        if i < start:
            continue

        yield ServerSentEvent(
            data=item,
            id=str(i),
        )


# SSE는 GET만 가능한 것이 아님.
# POST를 포함한 다른 HTTP 메서드에서도 사용할 수 있음.
