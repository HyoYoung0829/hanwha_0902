questions = ["asyncio란?", "", "FastAPI란?"]
valid_questions: list[str] = []

for question in questions:

    # strip()은 문자열(string) 양쪽에 있는 공백(스페이스, 탭, 줄바꿈 등)을 제거해 주는 Python의 내장 문자열 메서드.
    cleaned = question.strip()
    if not cleaned:
        continue  # <--- cleaned가 빈 문자열("")이면, 이후 실행X, 3번째 요소를 실행.

    valid_questions.append(cleaned)

print(valid_questions)

# ['asyncio란?', 'FastAPI란?']

# asyncio
# 파이썬에서 비동기 처리를 할 때 사용하는 라이브러리
# JS의 async / await + 이벤트 루프 개념과 비슷함

# FastAPI
# 파이썬으로 API 서버를 빠르게 만들 수 있는 웹 프레임워크
# JS의 Express.js와 비슷한 역할
