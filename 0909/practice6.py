# 실제 회원 관리에서는 베이스모델을 사용해서 사용자 데이터의 검증도 하며 토큰을 같이 관리하는것이 중요해진다.

from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


# 하위 의존성
def fake_decode_token(token):
    return User(
        username=token + "fakedecode", email="john@naver.com", full_name="John Doe"
    )


# 토큰을 받아서 그걸로 복호화 함수를 실행.
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user


@app.get("/user/me")
async def read_user_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
