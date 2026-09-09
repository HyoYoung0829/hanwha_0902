# yield
# 작업 완료 후 추가 단계를 수행하는 의존성
# 각 의존성마다 yield는 한번만 사용 가능.
# Depends로 가져온 자원을 API가 다 쓴 뒤 정리까지 해야 할 때 yield를 사용한다고 함.

# 가정)
# DB 연결 생성
# → API에서 사용
# → API 작업 끝남
# → DB 연결 종료


async def get_db():
    # 디비 세션을 "db"라는 변수에 담고 yield로 넘김
    db = DBSession()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/")
# 그럼 여기서 받아서 사용함.
async def get_users(db=Depends(get_db)):
    return db.get_users()


# 내부적으로는 이런식으로 동작함.
# 1. get_db 실행
# 2. DBSession 생성
# 3. yield db
# 4. FastAPI가 db를 get_users에 넣음
# 5. get_users 실행
# 6. 응답 처리
# 7. 다시 get_db로 돌아옴
# 8. finally 실행
# 9. db.close()

# 실제로는 yield를 만나면 해당 함수는 "일시정지" 처리가 되고 나중에 다시 이어서 실행되는 원리임.

# 해커톤에서 어떻게 활용할 수 있는가?
# => Agent 대화 기록을 SQL DB에 저장한다고 할때 db 세션을 관리할때 도움됨.
