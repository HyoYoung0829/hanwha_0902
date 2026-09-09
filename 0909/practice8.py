# SQLModel
# 이전 배운 내용들은 클라이언트 <-> 서버 간의 통신이었다면,
# 이번에는 서버 <-> DB 간의 통신을 배움.

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select


# SQLModel + table=True
# → Python 클래스를 실제 DB 테이블과 연결한다.
class Hero(SQLModel, table=True):
    # primary_key=True
    # → 각 row를 구분하는 고유 id
    id: int | None = Field(default=None, primary_key=True)

    # 일반 컬럼
    name: str
    age: int | None = None
    secret_name: str


# 개념적으로:
# Hero 클래스   ↔ hero 테이블
# Hero 객체 1개 ↔ DB row 1개


# SQLite DB 주소
sqlite_url = "sqlite:///database.db"

# engine
# → 애플리케이션이 어떤 DB를 사용할지 연결 정보를 관리하는 객체
# → 보통 앱 전체에서 하나 만들어 공유한다.
engine = create_engine(
    sqlite_url,
    connect_args={"check_same_thread": False},
)


# Session
# → 실제로 DB 조회/저장/수정/삭제를 수행하는 작업 객체
#
# yield를 사용하는 이유:
# 요청 동안 session을 빌려주고,
# 요청이 끝나면 with문이 종료되면서 session도 정리된다.
def get_session():
    with Session(engine) as session:
        yield session


# 매번 아래처럼 쓰는 걸 줄이기 위한 별칭
# Annotated[Session, Depends(get_session)]
SessionDep = Annotated[Session, Depends(get_session)]


app = FastAPI()


# 서버 시작 시 SQLModel 모델을 기준으로 DB 테이블을 생성한다.
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


# CREATE
@app.post("/heroes/")
# "이 파라미터는 그냥 일반 값이 아니라
# get_session 의존성에서 받아와야 하는 값이구나~"
def create_hero(hero: Hero, session: SessionDep):
    # 저장할 객체를 Session에 등록
    session.add(hero)

    # 변경사항을 실제 DB에 반영
    session.commit()

    # DB에서 생성된 id 등 최신 값을 다시 hero 객체에 반영
    session.refresh(hero)

    return hero


# READ - 전체 조회
@app.get("/heroes/")
def read_heroes(session: SessionDep):
    # select(Hero)
    # → Hero 테이블 조회 쿼리 생성
    #
    # session.exec(...)
    # → 쿼리 실행
    #
    # .all()
    # → 조회 결과 전체 가져오기
    return session.exec(select(Hero)).all()


# READ - 하나 조회
@app.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: SessionDep):
    # Primary Key를 기준으로 Hero 하나 조회
    hero = session.get(Hero, hero_id)

    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    return hero


# DELETE
@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)

    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    # 삭제 대상으로 등록
    session.delete(hero)

    # 실제 DB에 삭제 반영
    session.commit()

    return {"ok": True}


# 핵심 흐름
#
# Client
#   ↓ HTTP 요청
# FastAPI
#   ↓
# Session
#   ↓
# Engine
#   ↓
# Database
#
#
# 역할 정리
#
# SQLModel
# → Python 모델과 DB 테이블을 연결
#
# Engine
# → DB 연결 정보 관리
#
# Session
# → 실제 CRUD 작업 수행
#
# Depends(get_session)
# → API 요청마다 Session을 받아서 사용
#
#
# 자주 쓰는 메서드
#
# session.add()     → 저장할 객체 등록
# session.commit()  → 변경사항 DB 반영
# session.refresh() → DB의 최신 값 다시 반영
# session.get()     → Primary Key로 하나 조회
# select()          → 조회 쿼리 생성
# session.delete()  → 삭제
