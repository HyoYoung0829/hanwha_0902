from fastapi import FastAPI

# 내가 가져올 api들.
from routers import agents, users

app = FastAPI()

# 가져와서 연결.
app.include_router(users.router)
app.include_router(agents.router)


@app.get("/")
def root():
    return {"message": "Hello FastAPI"}


# 전체 구조도
# practice9/
# │
# ├── main.py
# │     └─ FastAPI 생성
# │        Router들을 합침
# │
# ├── dependencies.py
# │     └─ 공통 의존성
# │
# └── routers/
#       │
#       ├── users.py
#       │     └─ 사용자 API
#       │
#       └── agents.py
#             └─ Agent API


# 실행 방법
# cd 0909/practice9
# python3 -m uvicorn main:app --reload
