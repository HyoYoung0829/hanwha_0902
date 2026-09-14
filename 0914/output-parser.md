# Output Parser 정리

## 1. Output Parser란?

LLM의 출력 결과를 **프로그램에서 사용하기 좋은 형태로 변환하는 도구**이다.

LLM은 기본적으로 텍스트를 생성하므로, 필요에 따라 문자열, 리스트, JSON, Pydantic 객체 등으로 변환해서 사용할 수 있다.

```text
LLM 출력
   ↓
Output Parser
   ↓
원하는 Python 데이터 형태
```

---

## 2. 주요 Output Parser

### StrOutputParser

LLM의 응답에서 텍스트만 꺼내 문자열로 반환한다.

```python
parser = StrOutputParser()
```

```text
결과 → "RAG는 검색 증강 생성입니다."
```

**사용:** 일반적인 자연어 답변

---

### JsonOutputParser

LLM이 생성한 JSON 형태의 텍스트를 Python의 `dict` 같은 JSON 객체로 변환한다.

```python
parser = JsonOutputParser()
```

```json
{
  "name": "철수",
  "age": 25
}
```

```python
# 결과
{"name": "철수", "age": 25}
```

**사용:** 여러 데이터를 구조적으로 받고 싶을 때

---

### PydanticOutputParser

Pydantic 모델을 기준으로 LLM의 출력을 파싱하고 검증한다.

```python
class User(BaseModel):
    name: str
    age: int

parser = PydanticOutputParser(
    pydantic_object=User
)
```

```python
# 결과
User(name="철수", age=25)
```

**사용:** 출력 구조와 타입을 엄격하게 관리하고 싶을 때

#### JsonOutputParser와 차이

```text
JsonOutputParser
→ JSON 구조이면 됨

PydanticOutputParser
→ JSON 구조 + 내가 정의한 필드와 타입까지 검증
```

---

### List 계열 Parser

LLM의 목록 형태 출력을 Python 리스트로 변환한다.

#### CommaSeparatedListOutputParser

```text
apple, banana, orange
```

↓

```python
["apple", "banana", "orange"]
```

#### NumberedListOutputParser

```text
1. apple
2. banana
3. orange
```

↓

```python
["apple", "banana", "orange"]
```

#### MarkdownListOutputParser

```text
- apple
- banana
- orange
```

↓

```python
["apple", "banana", "orange"]
```

**사용:** 여러 항목을 리스트로 받고 싶을 때

---

### EnumOutputParser

미리 정해둔 선택지 중 하나를 반환하게 할 때 사용한다.

```python
class Sentiment(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
```

```text
결과 → positive
```

**사용:** 감정 분류, 카테고리 분류 등

---

### XMLOutputParser

LLM의 XML 형태 출력을 파싱한다.

```xml
<user>
    <name>철수</name>
    <age>25</age>
</user>
```

**사용:** XML 형식이 필요한 시스템

일반적인 웹/AI 서비스에서는 JSON이나 Pydantic을 더 자주 사용한다.

---

## 3. get_format_instructions()

Output Parser가 원하는 출력 형식을 **LLM에게 설명하기 위한 안내문을 생성하는 메서드**이다.

```python
parser.get_format_instructions()
```

이 메서드 자체가 LLM을 호출하는 것은 아니다.

LangChain 라이브러리 내부에 정의된 규칙과 스키마 정보를 바탕으로 문자열을 만든다.

```text
"이런 형식으로 출력하세요."
```

이 안내문을 프롬프트에 포함시켜 LLM이 원하는 형식으로 답하도록 유도할 수 있다.

---

## 4. parse()

LLM이 생성한 텍스트를 실제 Python 데이터 구조로 변환하는 메서드이다.

```python
text = '{"name": "철수", "age": 25}'

result = parser.parse(text)
```

```python
# 결과
{"name": "철수", "age": 25}
```

`parse()` 과정에서는 일반적으로 LLM이 다시 호출되지 않는다.

---

## 5. 전체 흐름

```text
프롬프트
   ↓
LLM
   ↓
텍스트 출력
   ↓
Output Parser
   ↓
Python 데이터
```

예를 들어:

```python
chain = prompt | model | parser
```

```text
prompt
→ LLM 입력 생성

model
→ 답변 생성

parser
→ 답변 후처리
```

---

## 6. 간단 비교

| Parser | 결과 | 특징 |
|---|---|---|
| `StrOutputParser` | `str` | 일반 텍스트 |
| `JsonOutputParser` | `dict` 등 | JSON 구조 |
| `PydanticOutputParser` | Pydantic 객체 | 구조 + 타입 검증 |
| List Parser | `list` | 목록 형태 |
| `EnumOutputParser` | Enum 값 | 정해진 값 중 하나 |
| `XMLOutputParser` | XML 구조 | XML 형식 |

---

## 7. 핵심 정리

```text
Str
→ 그냥 글

List
→ 목록

JSON
→ 자유로운 구조 데이터

Pydantic
→ 구조 + 타입 검증

Enum
→ 정해진 선택지 중 하나
```

Output Parser의 핵심 역할은 **LLM의 텍스트 출력을 프로그램에서 다루기 좋은 형태로 변환하는 것**이다.
