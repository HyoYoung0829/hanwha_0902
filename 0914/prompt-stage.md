# Prompt 단계 정리

## 1. Prompt 단계란?

RAG에서 Prompt 단계는 **검색된 정보와 사용자의 질문, LLM이 따라야 할 규칙을 하나의 입력으로 조립하는 단계**이다.

```text
사용자 질문
   ↓
Embedding
   ↓
Vector DB 검색
   ↓
관련 문서 검색
   ↓
Prompt 구성
   ↓
LLM
   ↓
답변 생성
```

즉, 검색된 문서를 LLM에게 그냥 전달하는 것이 아니라,

- 어떤 역할을 해야 하는지
- 어떤 자료를 참고해야 하는지
- 사용자가 무엇을 물었는지
- 어떤 규칙을 따라야 하는지

를 정리해서 LLM에게 전달한다.

---

## 2. Prompt에 들어가는 주요 요소

### 1) 역할 / 규칙

LLM이 어떤 역할을 하고 어떻게 답해야 하는지 지정한다.

```text
너는 사내 규정에 답변하는 AI이다.
반드시 제공된 context를 기준으로 답변한다.
모르는 내용은 추측하지 않는다.
```

주로 `system` 메시지에 작성한다.

---

### 2) Context

Retriever가 검색한 관련 문서나 데이터를 넣는다.

```text
Context:
미사용 연차는 최대 5일까지 다음 연도로 이월할 수 있다.
```

RAG에서 가장 중요한 외부 지식 입력이다.

---

### 3) 사용자 질문

사용자가 실제로 무엇을 알고 싶은지 전달한다.

```text
Question:
연차는 며칠까지 이월할 수 있어?
```

사용자 질문은 보통 두 번 사용된다.

```text
사용자 질문
   ├─ Embedding → 관련 문서 검색
   └─ Prompt → LLM이 무엇에 답해야 하는지 판단
```

---

### 4) 대화 기록

대화형 서비스라면 이전 질문과 답변을 함께 넣을 수 있다.

```text
Human: RAG가 뭐야?
AI: 검색 결과를 활용해 답변하는 방식이야.
Human: 그럼 검색은 어떻게 해?
```

LangChain에서는 `MessagesPlaceholder`를 사용해 이전 메시지들을 넣을 수 있다.

---

## 3. ChatPromptTemplate

LangChain에서 대화형 Prompt 구조를 만들 때 주로 사용한다.

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 RAG 선생님이야."),
    ("human", "{question}")
])
```

`from_messages()`는 여러 메시지를 역할별로 구성해서 하나의 Prompt Template으로 만들어준다.

```text
system
→ 역할 / 규칙 / 배경

human
→ 사용자 입력

ai
→ 이전 AI 답변
```

---

## 4. MessagesPlaceholder

여러 개의 메시지를 나중에 한 번에 넣기 위한 자리이다.

```python
from langchain_core.prompts import MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 RAG 선생님이야."),
    MessagesPlaceholder("history"),
    ("human", "{question}")
])
```

일반 변수:

```python
"{question}"
```

→ 문자열 하나를 넣는 자리

`MessagesPlaceholder`:

```python
MessagesPlaceholder("history")
```

→ 여러 개의 대화 메시지를 넣는 자리

---

## 5. RAG Prompt 예시

```python
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        너는 회사 규정에 답변하는 AI야.
        아래 context를 참고해서 답변해.
        context에 없는 내용은 추측하지 마.

        Context:
        {context}
        """
    ),
    ("human", "{question}")
])
```

실행 시:

```python
prompt.invoke({
    "context": "미사용 연차는 최대 5일까지 이월할 수 있다.",
    "question": "연차는 며칠까지 이월돼?"
})
```

LLM은 개념적으로 다음과 같은 입력을 받는다.

```text
[System]

너는 회사 규정에 답변하는 AI야.
아래 context를 참고해서 답변해.
context에 없는 내용은 추측하지 마.

Context:
미사용 연차는 최대 5일까지 이월할 수 있다.

[Human]

연차는 며칠까지 이월돼?
```

---

## 6. Prompt 단계에서 신경 써야 할 것

### 역할을 명확하게 작성하기

너무 추상적인 역할보다 실제 행동 기준을 작성하는 것이 좋다.

```text
X
너는 친절한 AI야.

O
너는 회사 규정 문서를 기준으로 직원 질문에 답변하는 AI야.
```

---

### Context 사용 규칙을 명확하게 작성하기

RAG에서는 LLM이 자신의 기존 지식보다 검색 결과를 우선하도록 해야 한다.

```text
제공된 context를 기준으로 답변하세요.
context에 없는 정보는 추측하지 마세요.
```

---

### 사용자 질문과 Context를 구분하기

둘을 명확하게 분리하면 LLM이 각 정보의 역할을 이해하기 쉽다.

```text
Context:
{context}

Question:
{question}
```

---

### 너무 많은 정보를 넣지 않기

Context를 많이 넣는다고 항상 좋은 것은 아니다.

관련 없는 문서가 많이 들어가면:

```text
검색 결과 증가
→ Prompt 길이 증가
→ 비용 증가
→ 핵심 정보가 묻힐 수 있음
```

따라서 Retriever 단계에서 관련성이 높은 문서를 가져오는 것이 중요하다.

---

### 모호한 지시를 줄이기

```text
X
잘 답변해줘.

O
제공된 context만 사용해서 3문장 이내로 답변해.
정보가 없으면 "확인할 수 없습니다."라고 답변해.
```

구체적인 규칙일수록 출력 결과가 안정적이다.

---

### 대화 기록을 무조건 많이 넣지 않기

대화 기록도 Context처럼 길어질 수 있다.

오래된 대화까지 계속 넣으면:

```text
Prompt 길이 증가
→ 비용 증가
→ 중요한 현재 질문이 묻힐 수 있음
```

필요한 대화만 유지하거나 요약해서 사용하는 방법을 고려할 수 있다.

---

## 7. Prompt 단계에서 LLM은 언제 등장하는가?

기본적인 RAG에서는 보통 검색 단계까지 LLM이 직접 관여하지 않는다.

```text
사용자 질문
   ↓
Embedding Model
   ↓
Vector DB
   ↓
관련 문서 검색
   ↓
Prompt 구성
   ↓
LLM 등장
   ↓
답변 생성
```

즉 기본 RAG에서는:

```text
Embedding + Vector DB
→ 어떤 자료를 찾을지 결정

Prompt
→ 찾은 자료와 질문을 정리

LLM
→ 그 자료를 바탕으로 답변 생성
```

---

## 8. 핵심 흐름

```text
사용자 질문
        ↓
Embedding
        ↓
Vector DB 검색
        ↓
관련 문서
        ↓
┌──────────────────────┐
│       Prompt         │
│                      │
│ 역할 / 규칙          │
│ Context              │
│ 대화 기록(optional)  │
│ 사용자 질문          │
└──────────────────────┘
        ↓
       LLM
        ↓
      답변
```

---

## 9. 핵심 정리

Prompt 단계의 핵심은 **LLM에게 어떤 정보를 어떤 역할로 전달할지 설계하는 것**이다.

```text
역할 / 규칙
→ LLM이 어떻게 행동할지 결정

Context
→ 답변에 사용할 외부 지식

사용자 질문
→ 무엇에 답해야 하는지 전달

대화 기록
→ 이전 맥락이 필요한 경우 사용
```

RAG에서는 검색 성능뿐 아니라 Prompt 구성도 답변 품질에 큰 영향을 준다.
