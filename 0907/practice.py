from datetime import datetime
from pydantic import BaseModel, PositiveInt, ValidationError

# 터미널에서 dict 구조를 읽기 편하게 하기 위해서.
from pprint import pprint


# id = 정수형
# name = 문자열인데 디폴트 값은 "백효영"
# signup_ts = date타입인데 None이 들어올 수 있음. 인자 생략이 되는건 아님.
# tastes = 키는 문자열, 밸류는 양의정수.
class User(BaseModel):
    id: int
    name: str = "백효영"
    signup_ts: datetime | None
    tastes: dict[str, PositiveInt]


# 외부에서 들어오는 데이터라고 가정하고 오브젝트 하나 만듬.
external_data = {
    "id": "000829",
    "signup_ts": "2026-09-07 10:08",
    "tastes": {
        "wine": 9,
        b"cheese": 7,
        "cabbage": "1",
        "burger": "10",
    },
}

error_external_data = {
    "id": "한글이지롱",
    "signup_ts": "이것도 타임스탬프 아니지롱",
    "name": "1029098235",
    "tastes": {"사과": 4, "배": 5, "오렌지": 6, "피자": "맛있어"},
}


# js의 스프레드 문법과 비슷하지만 살짝 다르다고 함.
# User 클래스에 '외부 데이터'를 주입해서 "검증"된 객체를 만들겠다! 라는 의미.
# 왜? User 클래스는 pydantic를 상속받아 만들어진 클래스임. 그래서 검증 단계가 끼게 됨.
# 외부 데이터의 순서가 바뀌어도 "키"를 바탕으로 매칭하기 때문에 순서는 상관 없다.
# "**"를 사용해서 딕트를 풀어줘야 User 클래스는 필요한 인자를 받을 수 있음.
user = User(**external_data)

# 만들어진 객체의 데이터 호출.
print(user.id)
print(user.model_dump())

print("---------------------------------------------------")


# JS의 try-catch 구문과 같음.
# 에러를 마주하면 pydantic의 VaildationError의 메서드를 통해 어디서 어떤 에러가 발생했는지 출력할 수 있다.
try:
    User(**error_external_data)
except ValidationError as e:
    pprint(e.errors())
