# 보안
# "보호된 API에서 Bearer 토큰을 어떻게 꺼내는가"

from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


# token 값을 받아오기 위해 oauth2_scheme 의존성을 실행한다.
# oauth2_scheme은 요청의 Authorization: Bearer <token> 헤더에서 token 값을 추출한다.
# tokenUrl="token"은 사용자가 토큰을 발급받을 API 엔드포인트가 /token이라는 뜻이다.
# 단, 이 코드는 /token API를 자동으로 만들어주지는 않는다.
# tokenUrl을 미리 지정하는 이유 중 하나는 Swagger/OpenAPI가 OAuth2 인증 흐름을 알 수 있게 하기 위해서다.
# 추출된 token 값은 read_items의 token 매개변수에 들어가고, 여기서는 그 값을 그대로 반환한다.
