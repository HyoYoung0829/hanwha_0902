# 1. 기본: 데이터 검증과 타입 변환

from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int
    email: str = None


user = User(
    name="백효영",
    age="26",
    email="gydud7300@naver.com",
)

print(user)
print(user.age)
print(type(user.age))
# >>>
# name='백효영' age=26 email='gydud7300@naver.com'
# 26
# <class 'int'>
