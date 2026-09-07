from datetime import datetime

from pydantic import BaseModel


class Meeting(BaseModel):
    when: datetime
    where: bytes
    why: str = "No idea"


m = Meeting(when="2020-01-01T12:00", where="home")

# "model_dump" Pydantic 모델 객체를 일반 Python dict로 바꾸는 메서드
# "exclude_unset" model_dump() 할 때 “사용자가 직접 넣지 않은 기본값 필드는 빼라
print(m.model_dump(exclude_unset=True))
# > {'when': datetime.datetime(2020, 1, 1, 12, 0), 'where': b'home'}

# "exclude={"where"}" → where 필드는 결과에서 빼라
# "mode" JSON에 넣기 쉬운 값 형태로 변환해서 dict로 내보내라
print(m.model_dump(exclude={"where"}, mode="json"))
# > {'when': '2020-01-01T12:00:00', 'why': 'No idea'}

# "exclude_defaults" 현재 값이 그 필드의 기본값과 같으면 dump 결과에서 빼라
print(m.model_dump_json(exclude_defaults=True))
# > {"when":"2020-01-01T12:00:00","where":"home"}
