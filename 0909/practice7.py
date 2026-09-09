# CORS
# 브라우저는 보안상 다른 출처로 JS 요청을 보내는 걸 기본적으로 제한함.
# => 브라우저에서 서로 다른 Origin끼리 통신할 때 발생하는 보안 정책.

# Origin = 프로토콜 + 도메인 + 포트
# localhost:3000과 localhost:8000도 서로 다른 Origin.


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 이런식으로 프론트 브라우저 요청을 미리 등록할 수 있음.
# 이 요청에서 오는건 허용하는거임.
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

# 미들웨어를 통해서 전처리를 할 수 있음.
app.add_middleware(
    CORSMiddleware,
    # 어떤 브라우저 요청을 허용할것인가?
    allow_origins=origins,
    # 쿠키 같은 인증 정보를 포함한 요청을 허용할것인가?
    allow_credentials=True,
    # 어떤 HTTP Method를 허용할것인가?
    allow_methods=["*"],
    # 프론트가 어떤 HTTP Header를 보내도 허용.
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}
