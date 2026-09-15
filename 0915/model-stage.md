# Model 단계 정리

> 기준 시점: 2026-09-15  
> 이 문서는 RAG 학습 과정에서 **Model 단계**를 중심으로 정리한 학습 노트이다.  
> 교재가 약 1년 전 기준이므로, 현재는 레거시가 된 기능과 최신 권장 패턴을 함께 표시한다.

---

## 1. RAG 파이프라인에서 Model의 위치

기본적인 RAG 흐름은 다음과 같다.

```text
원본 문서
↓
Document Loader
↓
Text Splitter
↓
Chunk
↓
Embedding
↓
Vector Store
↓
Retriever
↓
Prompt
↓
Model
↓
Output Parser
↓
최종 응답
```

Model 단계는 **검색된 문서와 사용자 질문이 조립된 Prompt를 실제로 읽고 답변을 생성하는 단계**이다.

```text
Prompt
= "무엇을 어떤 규칙으로 답할지 정리"

Model
= Prompt를 읽고 실제 답변 생성

Output Parser
= 모델의 출력을 프로그램이 쓰기 좋은 형태로 후처리
```

LangChain에서는 보통 다음처럼 연결한다.

```python
chain = prompt | model | parser
```

이때 `|`를 이용해 Runnable을 연결하는 문법을 **LCEL(LangChain Expression Language)** 이라고 한다.

### 주의: 생성 모델과 임베딩 모델은 다르다

RAG에서 "모델"이라는 말은 두 종류로 쓰일 수 있다.

```text
Embedding Model
→ 문서/질문을 벡터로 변환
→ 검색 단계에서 사용

LLM / Chat Model
→ 검색 결과와 질문을 읽고 답변 생성
→ 생성 단계에서 사용
```

---

# 2. 다양한 LLM 모델 / 플랫폼

## OpenAI - GPT

대표적인 상용 LLM 계열이다.

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="...")
```

특징:

- API 기반 사용이 일반적
- 텍스트, 이미지, 도구 호출, 구조화 출력 등 다양한 기능 지원
- LangChain과의 연동이 잘 되어 있음

활용 예시:

```text
일반 챗봇
RAG 답변 생성
Agent
코드 생성
구조화 데이터 추출
```

---

## Anthropic - Claude

Anthropic에서 제공하는 LLM 계열이다.

```python
from langchain_anthropic import ChatAnthropic
```

특징:

- 긴 문서 처리와 복잡한 텍스트 작업에 자주 사용
- tool calling, structured output 등 지원
- LangChain에서 대표적인 외부 모델 provider 중 하나

활용 예시:

```text
긴 문서 요약
문서 분석
Agent
RAG
코딩 보조
```

---

## DeepSeek

DeepSeek에서 제공하는 LLM 계열이다.

특징:

- reasoning, coding 계열 모델로 많이 알려져 있음
- 일부 모델은 open-weight 형태로 제공
- API 호출 또는 직접 호스팅 형태로 사용할 수 있음

활용 예시:

```text
코드 생성
추론 작업
비용을 고려한 LLM 서비스
자체 호스팅
```

---

## Cohere

기업용 NLP / LLM 서비스를 제공하는 회사이다.

특징:

- 생성형 모델뿐 아니라 **Embedding / Rerank** 계열도 많이 사용됨
- 특히 RAG에서는 reranker나 embedding 모델로 접할 가능성이 높음

활용 예시:

```text
RAG 문서 임베딩
검색 결과 재정렬(Rerank)
기업 문서 검색
텍스트 생성
```

RAG에서는 생성 모델보다 다음 위치에서 볼 가능성도 크다.

```text
Retriever
↓
검색 결과 여러 개
↓
Cohere Reranker
↓
관련성이 높은 문서 재정렬
↓
Prompt
```

---

## Upstage

국내 AI 기업으로 Solar 계열 모델과 Document AI 제품군을 제공한다.

특징:

- LLM
- Embedding
- Document Parse / OCR
- 문서 처리

등을 함께 제공한다.

활용 예시:

```text
한국어 문서 RAG
PDF / 스캔 문서 분석
OCR
문서 구조 분석
```

Upstage Document Parse는 단순 LLM 호출과는 다르다.

```text
PDF / 이미지
↓
OCR + 문서 구조 분석
↓
제목 / 문단 / 표 / 이미지 구조화
↓
RAG용 Document
```

---

## Meta - Llama

Llama는 **모델 자체**이다.

```text
Llama
= Meta가 개발한 LLM 계열
```

GPT4All이나 Ollama와 혼동하면 안 된다.

```text
Llama
→ 모델

Ollama / GPT4All
→ 모델을 로컬에서 실행하기 위한 도구
```

Llama 계열은 open-weight 형태로 제공되는 모델이 많아 직접 서버나 로컬 환경에서 실행할 수 있다는 특징이 있다.

활용 예시:

```text
사내망 LLM
로컬 LLM
자체 서버 운영
데이터 외부 전송이 어려운 서비스
```

---

## Hugging Face

Hugging Face는 특정 하나의 LLM 이름이 아니다.

```text
Hugging Face
= 다양한 AI 모델을 공유하고 실행할 수 있는 플랫폼 / 생태계
```

예를 들어 Hugging Face에서 다음과 같은 모델을 찾을 수 있다.

```text
Llama
Qwen
Mistral
Embedding Model
Vision Model
...
```

실행 방식도 다양하다.

```text
1. 모델을 다운로드해서 직접 실행

2. Hugging Face Inference API 사용

3. Hugging Face Endpoint에 모델을 배포해서 API 호출
```

### Endpoint란?

모델을 서버에 올려놓고 API 주소로 호출하는 방식이다.

```text
내 애플리케이션
↓
HTTP 요청
↓
Hugging Face Endpoint
↓
서버에 올라가 있는 모델
↓
응답
```

즉 OpenAI API처럼 사용할 수 있지만, **어떤 모델을 올릴지 직접 선택할 수 있다는 점**이 특징이다.

---

# 3. LLM 답변 캐싱

LLM Cache는 **동일한 모델 요청의 결과를 저장했다가 재사용하는 기능**이다.

```text
Prompt
↓
Model Wrapper
↓
Cache 조회
├─ HIT  → 저장된 응답 반환
└─ MISS → 실제 LLM API 호출
             ↓
          Cache 저장
```

캐시가 HIT하면 실제 LLM API 호출을 하지 않으므로:

```text
응답 속도 개선
API 비용 절약
```

효과가 있다.

---

## InMemoryCache

RAM에 캐시를 저장한다.

```python
from langchain_core.globals import set_llm_cache
from langchain_core.caches import InMemoryCache

set_llm_cache(InMemoryCache())
```

특징:

```text
빠름
간단함
프로그램 종료 시 사라짐
```

실습이나 테스트에 적합하다.

---

## SQLiteCache

캐시를 SQLite 파일에 저장한다.

```python
from langchain_core.globals import set_llm_cache
from langchain_community.cache import SQLiteCache

set_llm_cache(
    SQLiteCache(database_path="cache/langchain.db")
)
```

특징:

```text
프로그램을 종료해도 유지
별도 DB 서버 필요 없음
로컬 프로젝트에서 사용하기 편함
```

---

## Redis Cache

Redis 같은 외부 캐시 서버를 사용할 수도 있다.

```text
애플리케이션 여러 개
↓
공통 Redis
↓
LLM Cache 공유
```

서버 여러 대가 같은 캐시를 공유해야 하는 환경에 적합하다.

---

## Semantic Cache

일반 캐시는 보통 **정확히 같은 Prompt**에 대해 HIT한다.

```text
"아산 관광지 알려줘"
"아산 관광지 알려줘."
```

문자 하나만 달라도 다른 요청으로 취급될 수 있다.

Semantic Cache는 질문을 임베딩하여 의미적으로 비슷한 요청을 찾는다.

```text
"아산 관광지 알려줘"

≈

"아산에서 가볼 만한 곳 추천해줘"
```

장점:

```text
표현이 달라도 캐시 활용 가능
```

주의:

```text
의미가 비슷해도 상황에 따라 다른 답이 필요한 질문이라면
잘못된 캐시 응답을 사용할 위험이 있음
```

---

# 4. 직렬화와 역직렬화

## 직렬화(Serialization)

프로그램에서 사용 중인 객체를 **저장하거나 전달할 수 있는 형태로 변환하는 것**이다.

```text
Python 객체
↓
직렬화
↓
JSON / binary 등
```

예:

```python
user = {
    "name": "철수",
    "age": 25
}
```

이 객체를 JSON 문자열로 바꾸면 저장하거나 네트워크로 전달하기 쉬워진다.

---

## 역직렬화(Deserialization)

저장된 데이터를 다시 프로그램 객체로 복원하는 과정이다.

```text
JSON / binary
↓
역직렬화
↓
Python 객체
```

---

# 5. LangChain 객체 직렬화

LangChain에는 자체 직렬화 기능이 있다.

```python
from langchain_core.load import dumps, loads

serialized = dumps(prompt)
restored = loads(serialized)
```

또는 dict 형태로 만들 수 있다.

```python
from langchain_core.load import dumpd, load

data = dumpd(prompt)
restored = load(data)
```

### `is_lc_serializable()`

객체가 LangChain 직렬화 방식을 지원하는지 확인한다.

```python
prompt.is_lc_serializable()
```

```text
True
→ LangChain 직렬화 규약 지원

False
→ 그대로 직렬화하기 어려움
```

모든 Python 객체가 LangChain 방식으로 직렬화되는 것은 아니다.

예를 들어 사용자 정의 함수나 Lambda가 들어간 복잡한 체인은 직렬화가 어려울 수 있다.

---

## 체인 직렬화

예:

```python
chain = prompt | model
```

체인을 직렬화한다는 것은:

```text
Prompt 설정
Model 설정
Runnable 연결 구조
...
```

등을 저장하여 **나중에 같은 구조의 객체를 다시 구성**할 수 있게 하는 것이다.

주의할 점:

> 체인 직렬화는 LLM이 이미 생성한 답변을 저장하는 것이 아니다.

```text
체인 직렬화
→ 체인 구성 저장

LLM Cache
→ LLM 응답 저장
```

둘은 목적이 다르다.

### 실제 개발에서는?

작은 체인은 그냥 코드로 관리하는 경우가 많다.

```python
chain = prompt | model | parser
```

이 정도 체인은 직렬화 파일보다 코드 자체가 훨씬 명확하다.

---

# 6. Pickle 파일

Pickle은 Python 객체를 binary 형태로 직렬화하는 Python 기본 기능이다.

```python
import pickle

with open("object.pkl", "wb") as f:
    pickle.dump(obj, f)
```

불러오기:

```python
with open("object.pkl", "rb") as f:
    obj = pickle.load(f)
```

## Pickle이 유용한 경우

이미 계산이 끝난 객체 상태를 저장할 때 유용하다.

```text
원본 데이터
↓
전처리
↓
복잡한 객체 생성
↓
완성된 객체

        ↓ pickle

object.pkl

        ↓ 다음 실행

pickle.load()
↓
완성된 객체 바로 사용
```

예를 들어 머신러닝에서는:

```text
2시간 모델 학습
↓
학습 완료 모델 pickle 저장
↓
다음 실행에서 학습 과정 생략
```

과 같은 장점이 있다.

### LangChain 체인에서는?

```python
prompt | model | parser
```

같은 단순 체인은 생성 비용이 매우 작기 때문에 Pickle의 장점이 크지 않을 수 있다.

### 주의

**신뢰할 수 없는 Pickle 파일은 절대 `pickle.load()` 하지 않는다.**

Pickle 역직렬화 과정에서 임의 코드 실행 위험이 있기 때문이다.

또한 Pickle은 Python / 라이브러리 버전 의존성이 크기 때문에 장기 저장이나 시스템 간 교환 형식으로는 JSON 기반 설정이 더 관리하기 쉬운 경우가 많다.

---

# 7. 토큰 사용량 확인

LLM 사용 비용과 context 크기를 관리하려면 토큰 사용량을 확인하는 것이 중요하다.

## 한 번의 호출 확인

모델이 Usage Metadata를 제공한다면:

```python
response = model.invoke("RAG가 뭐야?")

print(response.usage_metadata)
```

예:

```python
{
    "input_tokens": 100,
    "output_tokens": 50,
    "total_tokens": 150
}
```

---

## 여러 모델 호출을 합산해서 확인

최신 LangChain에서는 provider 공통 Usage Metadata callback을 사용할 수 있다.

```python
from langchain_core.callbacks import get_usage_metadata_callback

with get_usage_metadata_callback() as cb:
    result = chain.invoke({
        "question": "RAG가 뭐야?"
    })

print(cb.usage_metadata)
```

이 방식은 `AIMessage.usage_metadata`를 제공하는 모델 integration에서 사용할 수 있다.

### 과거 OpenAI 전용 방식

교재에는 다음 코드가 있을 수 있다.

```python
from langchain_community.callbacks import get_openai_callback
```

`get_openai_callback()`은 OpenAI 중심의 기존 방식이다.

현재 새 코드를 작성한다면 가능하면:

```python
get_usage_metadata_callback()
```

처럼 provider 공통 방식부터 확인하는 것이 좋다.

---

# 8. Memory란?

LLM 자체는 기본적으로 이전 API 호출을 스스로 기억하지 않는다.

```text
1번째 호출
"내 이름은 철수야"

2번째 호출
"내 이름이 뭐였지?"
```

2번째 요청에 첫 번째 대화가 다시 전달되지 않으면 모델은 이전 내용을 알 수 없다.

Memory는 과거 정보를 저장했다가 다음 호출에 다시 제공한다.

```text
사용자 질문
↓
이전 Memory 불러오기
↓
Prompt에 history 삽입
↓
LLM
↓
답변
↓
현재 질문 + 답변 Memory 저장
```

핵심:

```text
LLM이 기억한다 X

애플리케이션이 과거 정보를 저장하고
다음 Prompt에 다시 넣어준다 O
```

---

# 9. 교재의 Memory 종류

> ⚠️ **2026 최신성 주의**
>
> 아래 `ConversationBufferMemory`, `ConversationEntityMemory` 같은 `Conversation*Memory` 클래스들은 현재 대부분 `langchain-classic`의 **Deprecated / 레거시 API**이다.
>
> 개념 자체는 여전히 중요하지만, 새 프로젝트에서는 뒤에서 설명할 **Message History / State / Checkpointer 방식**을 우선 고려한다.

---

## 9.1 ConversationBufferMemory

전체 대화 기록을 그대로 계속 저장한다.

```text
Human: 안녕
AI: 안녕하세요.

Human: RAG가 뭐야?
AI: ...

Human: 그럼 Embedding은?
AI: ...
```

특징:

```text
구현이 가장 단순
대화 내용 손실이 적음
대화가 길어지면 토큰 사용량 계속 증가
```

적합한 상황:

```text
짧은 챗봇 대화
간단한 실습
대화 턴 수가 많지 않은 서비스
```

---

## 9.2 ConversationBufferWindowMemory

최근 `k`개의 대화만 유지한다.

```text
전체 대화

1
2
3
4
5

k = 3

↓ 유지

3
4
5
```

특징:

```text
메모리 크기를 쉽게 제한
오래된 내용은 완전히 사라짐
```

적합한 상황:

```text
최근 맥락만 중요한 챗봇
고객 상담의 짧은 세션
```

---

## 9.3 ConversationTokenBufferMemory

대화 개수가 아니라 **토큰 수를 기준으로** 최근 메시지를 유지한다.

```text
max_token_limit = 2000

현재 history = 2300 tokens
↓
오래된 메시지 제거
↓
2000 tokens 이하 유지
```

특징:

```text
LLM Context Window를 직접 고려 가능
메시지 길이가 들쭉날쭉해도 관리하기 쉬움
오래된 정보는 사라짐
```

적합한 상황:

```text
토큰 비용을 일정 수준으로 제한하고 싶은 경우
긴 메시지가 자주 오가는 대화
```

---

## 9.4 ConversationEntityMemory

대화에서 **Entity(사람, 회사, 프로젝트, 장소 등)** 를 추출하고 해당 정보를 요약해서 기억한다.

예:

```text
"Planmingo는 내가 만든 여행 공동 편집 서비스야."
```

↓

```text
Entity: Planmingo

Summary:
사용자가 만든 여행 공동 편집 서비스
```

특징:

```text
전체 대화를 그대로 저장하지 않아도 됨
특정 대상에 대한 정보를 축적 가능
엔티티 추출 / 요약을 위해 LLM 호출이 추가될 수 있음
비용과 지연이 증가할 수 있음
```

적합한 상황:

```text
등장 인물이 많은 대화
프로젝트 / 회사 / 사람 정보가 반복되는 서비스
게임 NPC 대화
CRM형 AI
```

---

## 9.5 ConversationKGMemory

KG = Knowledge Graph

대화 속 Entity뿐 아니라 **Entity 사이의 관계**를 추출한다.

예:

```text
사용자는 Planmingo를 만들었다.
Planmingo는 여행 공동 편집 서비스다.
```

↓

```text
사용자 ──만들었다──> Planmingo

Planmingo ──종류──> 여행 공동 편집 서비스
```

특징:

```text
정보의 관계를 구조적으로 저장
복잡한 관계 질문에 유리할 수 있음
관계 추출 과정에서 LLM이 추가로 사용될 수 있음
구조가 복잡함
```

적합한 상황:

```text
사람 / 조직 / 프로젝트 관계 추적
세계관이 있는 서비스
관계 기반 질문이 많은 시스템
```

---

## 9.6 ConversationSummaryMemory

전체 대화 기록을 그대로 유지하지 않고 LLM으로 요약한다.

```text
대화 1
대화 2
대화 3
대화 4
        ↓
      LLM
        ↓
"사용자는 RAG를 공부하고 있으며
현재 Memory 파트를 학습 중이다."
```

특징:

```text
긴 대화를 압축할 수 있음
토큰 절약
요약 과정에서 LLM 호출 추가 가능
요약 과정에서 세부 정보가 손실될 수 있음
```

적합한 상황:

```text
긴 상담 세션
장시간 이어지는 챗봇
전체 흐름은 중요하지만 모든 문장이 필요하지 않은 경우
```

현재 LangChain에서도 **대화 요약이라는 전략 자체는 여전히 사용된다.**

다만 최신 방식에서는 `ConversationSummaryMemory` 대신 Agent의 state와 summarization 전략을 조합하는 방식이 더 자연스럽다.

---

## 9.7 VectorStoreRetrieverMemory

과거 대화를 Vector Store에 임베딩해서 저장하고, 현재 질문과 관련 있는 과거 기억만 Retriever로 검색한다.

```text
과거 대화
↓
Embedding
↓
Vector Store

현재 질문
↓
Embedding
↓
Memory Retriever
↓
관련 과거 대화 검색
↓
Prompt
```

특징:

```text
오래된 대화라도 의미적으로 관련 있으면 찾을 수 있음
대화를 전부 Prompt에 넣을 필요 없음
Embedding + Vector Store + Retriever가 필요
검색 품질에 영향을 받음
```

적합한 상황:

```text
장기 개인 비서
오래된 프로젝트 대화를 다시 찾아야 하는 서비스
장기 학습 튜터
많은 대화 기록을 가진 챗봇
```

RAG와 매우 비슷하다.

```text
일반 RAG Retriever
→ 외부 문서 검색

Memory Retriever
→ 과거 대화 검색
```

따라서 한 체인에서 Retriever가 두 종류 존재할 수도 있다.

```text
현재 질문
├─ RAG Retriever → 외부 지식
└─ Memory Retriever → 과거 대화

             ↓
           Prompt
             ↓
            LLM
```

---

# 10. Memory 방식 비교

| 방식 | 기억 기준 | 장점 | 단점 | 추가 LLM 호출 |
|---|---|---|---|---|
| Buffer | 전체 대화 | 단순, 정보 보존 | 토큰 증가 | X |
| Buffer Window | 최근 k개 | 간단한 크기 제한 | 오래된 정보 삭제 | X |
| Token Buffer | 토큰 제한 | Context 관리 용이 | 오래된 정보 삭제 | 보통 X |
| Entity | Entity별 요약 | 대상 중심 기억 | 추출/요약 비용 | O 가능 |
| Knowledge Graph | Entity 관계 | 관계 표현 가능 | 복잡함 | O 가능 |
| Summary | 대화 요약 | 토큰 절약 | 정보 손실 가능 | O |
| Vector Store | 의미 유사도 | 오래된 관련 기억 검색 | 검색 시스템 필요 | 검색 자체는 Embedding 중심 |

---

# 11. LCEL 체인에 Memory 추가

기본 LCEL 체인:

```python
chain = prompt | model | parser
```

이 체인 자체는 각 `invoke()`가 기본적으로 독립적이다.

Memory를 붙이면:

```text
실행 전
→ 이전 history 불러오기

체인 실행
→ history + 현재 질문 사용

실행 후
→ 현재 질문 + 답변 저장
```

이 과정이 자동화된다.

---

## RunnableWithMessageHistory

LCEL 체인에 메시지 기록을 붙이는 대표적인 방식이다.

```python
from langchain_core.runnables.history import RunnableWithMessageHistory
```

개념:

```text
RunnableWithMessageHistory

┌───────────────────────────────┐
│ 이전 대화 불러오기             │
│          ↓                    │
│ prompt → model → parser       │
│          ↓                    │
│ 이번 질문/답변 저장            │
└───────────────────────────────┘
```

Prompt에는 history가 들어갈 자리가 있어야 한다.

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 AI 튜터야."),
    MessagesPlaceholder("history"),
    ("human", "{question}")
])
```

기본 체인:

```python
chain = prompt | model
```

history 기능 추가:

```python
from langchain_core.runnables.history import RunnableWithMessageHistory

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)
```

호출할 때 session을 구분한다.

```python
chain_with_history.invoke(
    {"question": "내 이름은 철수야."},
    config={
        "configurable": {
            "session_id": "user-1"
        }
    }
)
```

---

# 12. 휘발성 Memory: 일반 변수 vs InMemory

둘은 사실 물리적으로는 둘 다 **RAM에 저장되는 휘발성 데이터**이다.

예를 들어 일반 Python 변수:

```python
history = []

history.append({
    "role": "user",
    "content": "안녕"
})
```

프로그램이 종료되면 사라진다.

---

## InMemoryChatMessageHistory

LangChain이 제공하는 메모리 기반 Message History 구현이다.

```python
from langchain_core.chat_history import InMemoryChatMessageHistory

history = InMemoryChatMessageHistory()
```

내부적으로는 결국 메시지를 메모리의 리스트에 저장한다.

차이는 저장 위치보다는 **인터페이스**이다.

```text
일반 list / dict
→ 내가 직접 저장 / 조회 / 변환 로직 구현

InMemoryChatMessageHistory
→ LangChain이 기대하는 BaseChatMessageHistory 인터페이스 제공
→ RunnableWithMessageHistory와 바로 연결하기 쉬움
```

즉:

```text
둘 다 RAM
둘 다 프로그램 종료 시 사라짐

하지만

일반 변수
→ 그냥 Python 데이터

InMemoryChatMessageHistory
→ LangChain 규격에 맞는 Memory 객체
```

---

# 13. SQLite에 대화 기록 저장

RAM이 아니라 SQLite 파일에 저장하면 프로그램을 종료해도 대화 기록이 유지된다.

LCEL + Message History에서는 `SQLChatMessageHistory`를 사용할 수 있다.

```python
from langchain_community.chat_message_histories import SQLChatMessageHistory

def get_session_history(session_id: str):
    return SQLChatMessageHistory(
        session_id=session_id,
        connection="sqlite:///chat_history.db",
    )
```

이 함수를 `RunnableWithMessageHistory`에 연결할 수 있다.

```python
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)
```

구조:

```text
사용자 질문
↓
session_id
↓
SQLite에서 해당 대화 조회
↓
Prompt history에 삽입
↓
LLM
↓
새 질문/답변 SQLite 저장
```

---

# 14. 최신 권장 패턴: Agent State + Checkpointer

> ⭐ **2026 기준 중요**

교재의 `ConversationBufferMemory`, `ConversationSummaryMemory` 같은 클래스는 개념을 이해하기에는 좋지만, 최신 LangChain / LangGraph 기반 Agent에서는 **Agent의 전체 상태(State)를 저장하고 복원하는 방식**이 중심이다.

기존 Memory가 주로 "대화 기록을 어떻게 기억할까?"에 집중했다면, 최신 방식은 더 넓게:

```text
"Agent가 다음 실행까지 어떤 상태를 유지해야 하는가?"
```

를 관리한다.

---

## 14.1 State란?

State는 **Agent가 현재 실행 과정에서 들고 있는 상태 데이터 전체**라고 보면 된다.

예를 들어:

```python
{
    "messages": [...],
    "user_id": "user-1",
    "preferences": {
        "language": "ko"
    },
    "current_task": "RAG 학습",
    "step": 3
}
```

처럼 대화 기록뿐 아니라 다양한 값을 함께 넣을 수 있다.

즉 기존 Memory와 비교하면:

```text
기존 Memory
→ 주로 과거 대화(history)를 기억

Agent State
→ 대화 기록 + 사용자 정보 + 작업 상태 + 중간 결과 등
   Agent가 다음 실행에서 이어가야 할 전체 상태
```

예를 들어 긴 Agent 작업에서:

```text
사용자 질문
↓
문서 검색 완료
↓
중간 분석 완료
↓
도구 호출 예정
```

같은 작업 진행 상태도 State로 관리할 수 있다.

---

## 14.2 Checkpointer란?

Checkpointer는 **Agent State를 저장하고 다음 실행에서 다시 불러오는 저장 계층**이다.

쉽게 말하면:

```text
State
= 무엇을 기억할 것인가

Checkpointer
= 그 State를 어디에 저장하고 어떻게 복원할 것인가
```

이다.

흐름:

```text
Agent 실행
↓
State 생성 / 변경
↓
Checkpointer에 저장
↓
실행 종료

        ...

다음 요청
↓
Checkpointer에서 이전 State 복원
↓
Agent가 이전 상태에서 계속 실행
```

---

## 14.3 thread_id

Checkpointer는 보통 **thread_id** 같은 식별자를 이용해 어떤 대화/작업의 State인지 구분한다.

예:

```text
thread_id = "user-1-chat-1"
```

첫 번째 요청:

```text
Human: 내 이름은 철수야.
↓
State.messages에 저장
↓
Checkpointer 저장
```

두 번째 요청에서 같은 `thread_id`를 사용하면:

```text
Human: 내 이름이 뭐였지?
↓
Checkpointer에서 이전 State 복원
↓
"내 이름은 철수야" 메시지를 다시 확인
↓
연속 대화 가능
```

즉 대화형 서비스에서는 `thread_id`가 하나의 대화 세션을 구분하는 키 역할을 한다.

---

## 14.4 InMemorySaver

개발이나 테스트에서는 메모리에 State를 저장할 수 있다.

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
```

특징:

```text
RAM에 저장
구성이 간단함
프로그램 종료 시 모두 사라짐
```

활용:

```text
학습
테스트
간단한 로컬 데모
```

---

## 14.5 SQLite Checkpointer

로컬 프로젝트나 작은 서비스에서는 SQLite 파일에 State를 저장할 수 있다.

개념:

```text
Agent State
↓
SQLite 파일
↓
프로그램 종료
↓
재실행
↓
이전 State 복원
```

특징:

```text
별도 DB 서버 불필요
파일 하나로 관리 가능
프로그램을 껐다 켜도 상태 유지
```

활용:

```text
개인 프로젝트
로컬 Agent
소규모 데모
프로토타입
```

---

## 14.6 PostgreSQL 등의 영속 저장소

서비스 규모가 커지면 여러 서버와 사용자가 상태를 공유해야 할 수 있다.

```text
Server A ─┐
Server B ─┼→ PostgreSQL Checkpointer
Server C ─┘
```

이 경우 SQLite보다 PostgreSQL 같은 중앙 DB가 적합하다.

활용:

```text
Production Agent
여러 서버가 동작하는 서비스
다수 사용자 세션 관리
장기간 상태 보존
```

---

## 14.7 왜 기존 Memory보다 확장된 방식인가?

기존에는 목적마다 별도의 Memory 클래스를 선택하는 방식이 많았다.

```text
ConversationBufferMemory
ConversationSummaryMemory
ConversationEntityMemory
ConversationKGMemory
...
```

최신 방식에서는 먼저 Agent의 상태를 하나의 State로 관리하고:

```text
State
+
Checkpointer
+
필요한 Memory 전략
```

을 조합한다.

예를 들어:

```text
최근 메시지만 남기고 싶다
→ messages trim

오래된 대화를 줄이고 싶다
→ summarization

관련 있는 오래된 기억을 찾고 싶다
→ Vector Store 연결

사용자별 대화를 유지하고 싶다
→ thread_id + Checkpointer

사용자 취향을 장기간 기억하고 싶다
→ 별도 long-term Store
```

즉:

```text
예전
→ "어떤 Memory 클래스를 쓸까?"

최신
→ "어떤 State를 유지하고,
   어떤 저장소에 보관하고,
   어떤 기억 전략을 조합할까?"
```

로 관점이 바뀐 것이다.

---

## 14.8 Short-term Memory와 Long-term Memory

최신 구조에서는 이 둘을 구분해서 보는 것이 좋다.

### Short-term Memory

현재 대화나 작업 세션 안에서 필요한 상태이다.

```text
최근 대화
현재 Tool 결과
Agent 진행 상태
```

주로:

```text
State + Checkpointer
```

로 관리한다.

---

### Long-term Memory

대화 세션이 달라져도 다시 활용해야 하는 정보이다.

예:

```text
사용자 선호도
장기 목표
과거 프로젝트 정보
오래된 중요한 기억
```

이런 정보는 별도 Store, DB, Vector Store 등에 저장하고 필요할 때 검색해서 사용한다.

```text
Short-term
→ 지금 이 대화를 이어가기 위한 기억

Long-term
→ 다음 주, 다음 달에도 다시 찾을 기억
```

---

## 14.9 전체 구조 예시

최신 Agent의 메모리 구조를 단순화하면:

```text
사용자 입력
↓
thread_id
↓
Checkpointer
↓
이전 Agent State 복원
↓
┌─────────────────────────┐
│ State                   │
│                         │
│ messages                │
│ user_id                 │
│ current_task            │
│ 기타 상태               │
└─────────────────────────┘
↓
Agent / Model 실행
↓
State 변경
↓
Checkpointer에 다시 저장
```

필요하다면 여기에 Long-term Memory를 추가한다.

```text
현재 질문
├─ State / Checkpointer
│   → 현재 세션의 최근 맥락
│
└─ Vector Store / DB
    → 오래된 장기 기억 검색

           ↓
        Agent / LLM
```

---

# 15. 기존 Memory와 최신 방식 비교

과거:

```text
ConversationBufferMemory
ConversationSummaryMemory
ConversationEntityMemory
...
```

현재:

```text
Agent State
↓
Checkpointer
↓
대화 / 작업 상태 저장

필요하면
├─ trim
├─ summarize
├─ vector search
├─ long-term store
└─ custom state
```

즉 예전에는 **Memory 종류마다 별도의 클래스**가 많았다면, 최근에는:

> **State를 중심으로 저장하고 필요한 기억 전략을 조합하는 방식**

에 가깝다.

---

# 16. Memory / Cache / Persistence 차이

세 개를 혼동하지 않는 것이 중요하다.

## Cache

```text
"같은 LLM 요청이 또 왔나?"
```

있으면 이전 LLM 응답을 재사용한다.

목적:

```text
비용 절감
응답 속도 개선
```

---

## Memory

```text
"이 사용자와 이전에 어떤 대화를 했지?"
```

과거 정보를 다음 LLM 호출에 제공한다.

목적:

```text
대화 연속성
사용자 / 세션 맥락 유지
```

---

## Persistence

```text
"프로그램을 껐다 켜도 데이터를 유지할 것인가?"
```

SQLite, PostgreSQL, Redis 등의 저장소를 사용한다.

```text
InMemory
→ 프로세스 종료 시 사라짐

SQLite / PostgreSQL
→ 재실행 후에도 유지
```

---

# 17. 오늘 단계에서 기억할 핵심

```text
Model
→ Prompt를 읽고 답변을 생성하는 단계

Cache
→ 동일한 LLM 요청의 결과 재사용

Serialization
→ 객체의 구조/상태를 저장 가능한 형태로 변환

Pickle
→ Python 객체 자체를 binary로 저장하는 방식

Token Usage
→ 비용과 Context 사용량 확인

Memory
→ 과거 대화를 저장하고 다음 호출에 다시 전달

LCEL + Memory
→ RunnableWithMessageHistory 등으로 체인을 감싸서
   history 읽기/쓰기를 자동화
```

최신 Agent 구조에서는:

```text
State
→ Agent가 유지해야 할 전체 상태

Checkpointer
→ State를 저장하고 복원

thread_id
→ 어떤 대화/작업의 State인지 구분
```

이라고 이해하면 된다.

---

# 18. 어떤 방식을 선택할까?

간단한 실습:

```text
InMemoryChatMessageHistory
```

간단한 LCEL 대화형 체인:

```text
RunnableWithMessageHistory
+
InMemoryChatMessageHistory
```

프로그램을 껐다 켜도 대화를 유지:

```text
RunnableWithMessageHistory
+
SQLChatMessageHistory(SQLite 등)
```

최신 Agent 개발:

```text
Agent State
+
Checkpointer
```

긴 대화:

```text
최근 메시지 유지
+
요약
```

오래된 특정 기억을 다시 찾아야 함:

```text
Vector Store / Long-term Memory
```

---

# 19. 최신성 참고

2026-09-15 기준 주요 흐름:

- `ConversationBufferMemory`, `ConversationBufferWindowMemory`, `ConversationTokenBufferMemory`, `ConversationEntityMemory`, `ConversationSummaryMemory`, `VectorStoreRetrieverMemory` 등 기존 `Conversation*Memory` API는 레거시 영역으로 이동한 상태이다.
- 최신 LangChain / LangGraph Agent의 short-term memory는 **Agent State + Checkpointer** 기반 방식이 중심이다.
- `State`는 단순 대화 기록뿐 아니라 사용자 정보, 작업 진행 상태, 도구 실행 결과 등 Agent가 유지해야 하는 전체 상태를 담을 수 있다.
- `Checkpointer`는 State를 저장하고 `thread_id`를 기준으로 다음 실행에서 복원한다.
- 개발 / 테스트에서는 InMemory 방식, 로컬 / 소규모 프로젝트에서는 SQLite, production에서는 PostgreSQL 같은 영속 저장소를 고려할 수 있다.
- 긴 대화는 메시지 trim, summarization 등의 전략을 State 위에 조합한다.
- 오래된 특정 기억을 다시 검색해야 할 경우 Vector Store나 별도 long-term Store를 함께 사용할 수 있다.
- `RunnableWithMessageHistory`는 일반 LCEL Runnable에 메시지 기록을 추가하는 용도로 사용할 수 있다.
- 토큰 사용량은 `AIMessage.usage_metadata` 및 `get_usage_metadata_callback()` 같은 공통 usage metadata 방식으로 확인할 수 있다.
- LangChain 직렬화는 `dumpd` / `dumps`와 `load` / `loads`를 제공한다.

## 참고 문서

- LangChain Short-term Memory  
  https://docs.langchain.com/oss/python/langchain/short-term-memory

- LangChain Long-term Memory  
  https://docs.langchain.com/oss/python/langchain/long-term-memory

- LangChain Serialization  
  https://reference.langchain.com/python/langchain-core/load

- RunnableWithMessageHistory  
  https://reference.langchain.com/python/langchain-core/runnables/history/RunnableWithMessageHistory

- Usage Metadata Callback  
  https://reference.langchain.com/python/langchain-core/callbacks/usage/get_usage_metadata_callback

- LangGraph Checkpoints  
  https://reference.langchain.com/python/langgraph/checkpoints
