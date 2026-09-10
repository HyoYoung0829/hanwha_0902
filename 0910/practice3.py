# 백그라운드
# 클라이언트에게는 응답을 먼저 보내고
# 시간이 오래걸리는 작업은 백그라운드에서 처리하는 기법.

from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


# fastapi는 "BackgroundTasks" 타입의 파라미터를 보면
# 알아서 BackgroundTasks 객체를 자동으로 만들어준다.


@app.post("/send-notification/{email}")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks,
):
    # write_notification()을 실행하지 말고, 응답을 보낸 뒤 실행할 작업으로 등록해~! 라는 의미.
    # 마찬가지로 함수를 실행하는게 아니라 함수 자체를 넘긴다.
    background_tasks.add_task(
        write_notification,
        email,
        message="some notification",
    )

    return {"message": "Notification sent in the background"}


# 실제 실행 순서
# 요청:
# POST /send-notification/test@test.com

# 이 들어오면:
# send_notification 실행
# → add_task로 write_notification 등록
# → return 실행
# → 클라이언트가 응답 받음
# → 그 후 write_notification 실행


# 백그라운드 함수는 def도 되고 async def도 가능하다.
# Depends 안에서도 사용 가능.

# 해커톤에서 어떻게 활용 가능?
# LLM 답변을 생성되는 대로 사용자에게 보여주고 싶다
# → SSE

# 답변을 다 보낸 뒤 대화 로그를 저장하거나 분석하고 싶다
# → BackgroundTasks

# 근데 만약에 백그라운드에서 처리하는 작업이 무겁다면
# fastapi 밖에서 처리하는게 권장사항.
