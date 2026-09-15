# 데이터 로드와 텍스트 분할 정리

> 기준 시점: 2026-09-15  
> 이 문서는 RAG에서 **원본 데이터를 읽고, 검색하기 좋은 Chunk로 만드는 전처리 단계**를 정리한 학습 노트이다.  
> 교재가 약 1년 전 기준이므로, 현재 패키지 위치나 권장 방식이 달라진 부분은 별도로 표시한다.

---

# 1. RAG 파이프라인에서 위치

전체 흐름에서 데이터 로드와 텍스트 분할은 가장 앞쪽의 **전처리 단계**에 위치한다.

```text
원본 데이터
↓
Document Loader
↓
Document 객체
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
```

즉 이 파트의 목적은:

```text
PDF / CSV / 웹페이지 / HWP / HTML / JSON ...
↓
LangChain이 다룰 수 있는 Document 형태로 통일
↓
검색하기 좋은 작은 단위로 분할
```

하는 것이다.

---

# 2. Document Loader란?

Document Loader는 **다양한 원본 데이터를 LangChain의 `Document` 객체로 변환하는 입구 역할**을 한다.

원본 데이터는 형태가 모두 다르다.

```text
PDF
TXT
CSV
웹페이지
HTML
HWP
DataFrame
JSON
...
```

하지만 이후 Embedding / Vector Store 단계에서는 일정한 형태로 다루는 것이 편하다.

그래서 Loader가 이를 공통 `Document` 구조로 바꿔준다.

```text
PDF ─┐
CSV ─┤
WEB ─┤
HWP ─┤
HTML ┤
     ↓
 Document
```

---

# 3. Document 객체란?

LangChain의 `Document`는 **본문 텍스트 + 메타데이터**를 저장하는 객체이다.

```python
from langchain_core.documents import Document

doc = Document(
    page_content="연차는 최대 5일까지 이월할 수 있다.",
    metadata={
        "source": "company_rule.pdf",
        "page": 12
    }
)
```

핵심 필드:

```text
page_content
→ 실제 검색 / 임베딩 대상이 되는 텍스트

metadata
→ 출처, 페이지, 제목, URL, 섹션 등의 부가 정보

id
→ 선택적으로 Document 식별자 사용 가능
```

예:

```python
print(doc.page_content)
print(doc.metadata)
```

```text
연차는 최대 5일까지 이월할 수 있다.

{
    "source": "company_rule.pdf",
    "page": 12
}
```

### metadata가 중요한 이유

RAG에서는 답변만 생성하는 것이 아니라 출처를 함께 보여줄 필요가 많다.

```text
검색된 Chunk
↓
metadata 확인
↓
출처: company_rule.pdf / 12페이지
```

따라서 문서를 로드할 때 metadata를 가능한 한 잘 유지하는 것이 좋다.

---

# 4. PDF Loader

PDF는 가장 자주 사용되는 RAG 데이터 형식 중 하나이다.

대표적인 로더:

```text
PyPDFLoader
PyMuPDFLoader
PDFPlumberLoader
PDFMinerLoader
UnstructuredPDFLoader
Document AI 기반 Parser
```

---

## PyPDFLoader

가장 기본적으로 사용하기 쉬운 PDF Loader 중 하나이다.

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("document.pdf")
docs = loader.load()
```

일반적으로 페이지 단위 `Document`로 읽을 수 있다.

활용:

```text
텍스트 중심 PDF
논문
간단한 보고서
```

주의:

```text
복잡한 표
다단 레이아웃
스캔 PDF
차트 / 이미지 중심 문서
```

는 텍스트 추출 품질이 떨어질 수 있다.

---

## PyMuPDFLoader

PyMuPDF 기반 PDF 로더이다.

장점:

```text
빠른 PDF 처리
이미지 추출 지원
표 추출 옵션 지원
레이아웃 관련 기능 활용 가능
```

활용:

```text
일반 PDF보다 구조가 조금 복잡한 문서
표 / 이미지가 있는 문서
빠른 로딩이 필요한 경우
```

---

## PDF Loader 선택 감각

```text
단순 텍스트 PDF
→ PyPDFLoader

조금 더 구조 / 표 / 이미지 처리 필요
→ PyMuPDFLoader

스캔 / 복잡한 레이아웃 / 문서 이해 필요
→ Upstage Document Parse / LlamaParse / Unstructured 계열
```

---

# 5. HWP Loader

HWP는 한국 기업 / 공공기관 데이터에서 자주 등장하지만, PDF나 DOCX보다 파싱 생태계가 복잡하다.

### 중요한 점

2026 기준 LangChain에서 **대표적인 전용 `HWPLoader`가 핵심 Loader로 널리 쓰이는 구조는 아니다.**

실무에서는 보통:

```text
HWP
↓
HWP 파서 / Document AI / Unstructured API
↓
text / markdown / html
↓
Document 객체 생성
```

형태로 처리한다.

Unstructured API는 현재 `.hwp`를 지원하는 파일 형식으로 명시하고 있다.

예:

```python
text = parse_hwp("document.hwp")

doc = Document(
    page_content=text,
    metadata={"source": "document.hwp"}
)
```

활용:

```text
공공기관 문서
사내 규정
정부 공고
계약서
한국어 기업 문서 RAG
```

### 주의

HWP는 단순 텍스트 평탄화만 하면:

```text
표 구조
문단 구조
제목 계층
양식 구조
```

가 깨질 수 있다.

따라서 복잡한 HWP 문서에서는 구조를 보존하는 parser를 선택하는 것이 중요하다.

---

# 6. CSV Loader

## CSVLoader

CSV 파일의 각 row를 `Document`로 읽는다.

```python
from langchain_community.document_loaders import CSVLoader

loader = CSVLoader("data.csv")
docs = loader.load()
```

예:

```csv
name,age,city
철수,25,서울
영희,24,부산
```

각 row가 개념적으로:

```text
name: 철수
age: 25
city: 서울
```

같은 `Document`가 된다.

활용:

```text
상품 목록
FAQ 데이터
직원 데이터
정형 테이블을 검색 데이터로 만들 때
```

---

## UnstructuredCSVLoader

Unstructured 라이브러리를 이용해 CSV를 문서 요소로 처리한다.

일반 `CSVLoader`는 주로 row 중심이고,

```text
CSVLoader
→ 각 row를 key/value 기반 텍스트로 변환
```

`UnstructuredCSVLoader`는:

```text
Unstructured
→ 표 문서로 해석
→ 구조 정보 활용
```

에 더 가깝다.

활용:

```text
단순 row 검색
→ CSVLoader

CSV 자체의 표 구조를 더 중요하게 다룰 때
→ UnstructuredCSVLoader
```

---

# 7. DataFrameLoader

이미 Pandas DataFrame을 가지고 있다면 파일로 다시 저장할 필요 없이 바로 `Document`로 변환할 수 있다.

```python
import pandas as pd
from langchain_community.document_loaders import DataFrameLoader

df = pd.DataFrame({
    "text": [
        "RAG는 검색 증강 생성이다.",
        "Embedding은 텍스트를 벡터로 변환한다."
    ]
})

loader = DataFrameLoader(
    df,
    page_content_column="text"
)

docs = loader.load()
```

활용:

```text
이미 pandas로 전처리가 끝난 데이터
DB 조회 결과를 DataFrame으로 만든 경우
CSV를 pandas에서 정제한 뒤 RAG에 넣는 경우
```

---

# 8. Lazy Loader

일반 `load()`는 데이터를 한 번에 메모리에 올린다.

```python
docs = loader.load()
```

문서가 매우 많으면 메모리를 많이 사용할 수 있다.

`lazy_load()`는 하나씩 순차적으로 가져온다.

```python
for doc in loader.lazy_load():
    print(doc)
```

흐름:

```text
load()

파일 10,000개
↓
전부 읽음
↓
메모리에 모두 저장
```

```text
lazy_load()

파일 10,000개
↓
하나 읽음
↓
처리
↓
다음 하나 읽음
```

활용:

```text
대규모 파일
메모리 절약
Streaming 방식 처리
문서를 읽는 즉시 Embedding하고 저장할 때
```

### 최신성

현재 LangChain Loader들은 `lazy_load()`를 광범위하게 지원하고 있으며,
대규모 ingestion에서는 `load()`보다 lazy 방식이 더 적합할 수 있다.

일부 Loader는 `alazy_load()`도 지원한다.

---

# 9. WebBaseLoader

웹페이지에서 텍스트를 읽어 `Document`로 만든다.

```python
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader(
    "https://example.com"
)

docs = loader.load()
```

내부적으로 HTML을 가져와 텍스트를 추출한다.

metadata에는 다음과 같은 정보가 포함될 수 있다.

```text
source
title
description
language
```

활용:

```text
공식 문서 RAG
블로그 검색
웹 기반 FAQ
웹페이지 QA
```

### 주의

JavaScript 렌더링이 필요한 웹페이지는 단순 HTTP Loader로 내용이 제대로 안 나올 수 있다.

이 경우:

```text
Playwright
Chromium
Browser 기반 Loader
```

가 필요할 수 있다.

---

# 10. DirectoryLoader

폴더 안의 여러 파일을 한꺼번에 읽는다.

```python
from langchain_community.document_loaders import DirectoryLoader

loader = DirectoryLoader(
    "./docs",
    glob="**/*.txt"
)

docs = loader.load()
```

다른 Loader와 조합할 수 있다.

```python
loader = DirectoryLoader(
    "./pdfs",
    glob="**/*.pdf",
    loader_cls=PyPDFLoader
)
```

활용:

```text
사내 문서 폴더 전체 ingestion
PDF 여러 개 일괄 처리
Knowledge Base 구축
```

주요 기능:

```text
glob
recursive
exclude
multithreading
lazy_load
```

---

# 11. UpstageDocumentParseLoader

Upstage의 Document Parse API를 이용해 문서를 구조적으로 분석하는 Loader이다.

```text
일반 Loader
→ 텍스트 추출 중심

Document Parse
→ 문서의 시각적 / 구조적 의미까지 분석
```

처리 흐름:

```text
PDF / 이미지
↓
OCR
↓
Layout Analysis
↓
제목 / 문단 / 표 / 차트 / 이미지 구분
↓
Markdown / HTML / Text
↓
Document
```

현재 Upstage LangChain integration에서는 다음 요소 유형들을 구분할 수 있다.

```text
table
figure
chart
heading
header
footer
caption
paragraph
equation
list
footnote
...
```

또한:

```text
OCR = auto / force
SplitType = none / page / element
OutputFormat = text / html / markdown
```

같은 옵션을 제공한다.

활용:

```text
스캔 문서
표가 많은 PDF
다단 문서
보고서
계약서
문서 레이아웃 보존이 중요한 RAG
```

### LLM이 관여하는가?

단순 LLM만으로 처리하는 것이 아니다.

```text
OCR 모델
+
문서 Layout 분석 모델
+
필요 시 VLM 계열 모델
```

등의 Document AI 기술이 관여할 수 있다.

즉:

```text
"GPT에게 PDF를 그냥 읽혀서 구조를 판단"
```

하는 방식과는 다르다.

---

# 12. LlamaParse

LlamaParse는 LlamaIndex 생태계의 문서 파싱 도구이다.

역할은 Upstage Document Parse와 비슷하게:

```text
복잡한 PDF / 문서
↓
구조 분석
↓
Markdown / 구조화된 결과
↓
RAG ingestion
```

에 사용된다.

특히:

```text
표
레이아웃
복잡한 문서
스캔 문서
```

를 일반 PDF Loader보다 더 구조적으로 변환하는 것이 목적이다.

### 중요한 구분

```text
Llama
→ Meta의 LLM

LlamaIndex
→ RAG / 데이터 프레임워크

LlamaParse
→ LlamaIndex 계열 문서 파서
```

서로 다른 개념이다.

### 최신성

LlamaParse는 LangChain core loader라기보다 **외부 문서 파싱 서비스 / LlamaIndex 생태계 도구**로 보는 것이 맞다.

LangChain에서 사용할 경우:

```text
LlamaParse로 문서 파싱
↓
텍스트 / Markdown 획득
↓
LangChain Document로 변환
↓
Splitter / Embedding
```

형태로 연결할 수 있다.

---

# 13. Loader 선택 기준

```text
TXT / 단순 파일
→ TextLoader

일반 PDF
→ PyPDFLoader / PyMuPDFLoader

복잡한 PDF / 스캔
→ Upstage Document Parse / LlamaParse / Unstructured

CSV 파일
→ CSVLoader

Pandas 처리 완료
→ DataFrameLoader

웹페이지
→ WebBaseLoader

폴더 전체
→ DirectoryLoader

HWP
→ HWP Parser / Unstructured API / Document AI
```

---

# 14. Text Splitter란?

Text Splitter는 `Document`의 본문을 **검색하기 좋은 작은 Chunk로 분할하는 도구**이다.

```text
Document

"100페이지짜리 회사 규정"

↓ Splitter

Chunk 1
Chunk 2
Chunk 3
...
```

이후 각각의 Chunk를 임베딩한다.

```text
Chunk
↓
Embedding
↓
Vector
↓
Vector Store
```

---

# 15. 왜 분할해야 하는가?

문서 전체를 하나의 벡터로 만들면 너무 많은 주제가 하나의 벡터에 섞인다.

```text
회사 규정 전체

연차
출장
복지
급여
인사
보안
...
```

사용자가:

```text
"연차 이월 규정 알려줘"
```

라고 해도 전체 문서 하나가 검색된다.

반면:

```text
Chunk 1 → 연차
Chunk 2 → 출장
Chunk 3 → 복지
...
```

로 나누면 연차 관련 Chunk만 찾을 수 있다.

---

# 16. Chunk Size와 Chunk Overlap

가장 기본적인 분할 옵션이다.

```python
chunk_size=500
chunk_overlap=100
```

### chunk_size

한 Chunk의 최대 크기 기준이다.

```text
Chunk 1 → 약 500자
Chunk 2 → 약 500자
...
```

### chunk_overlap

Chunk 사이에 일부 내용을 겹치게 한다.

```text
Chunk 1
AAAAAAAA BBBBBBBB

Chunk 2
BBBBBBBB CCCCCCCC
```

이유:

```text
문장이 Chunk 경계에서 끊기는 문제 완화
문맥 연결 유지
```

---

# 17. 정해진 Chunking 정답은 없다

Chunking은 문서와 질문 유형에 따라 최적값이 다르다.

```text
너무 작음
→ 검색은 세밀함
→ 문맥 부족

너무 큼
→ 문맥 풍부
→ 관련 없는 정보도 포함
→ 검색 정밀도 저하 가능
```

그래서 실제 RAG에서는:

```text
chunk_size
chunk_overlap
splitter 종류
retrieval k
```

를 바꿔가며 평가한다.

---

# 18. 문자 단위 분할

## CharacterTextSplitter

지정한 separator를 기준으로 텍스트를 나눈다.

```python
from langchain_text_splitters import CharacterTextSplitter

splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=500,
    chunk_overlap=50
)
```

예:

```text
문단 1

문단 2

문단 3
```

`\n\n` 기준으로 분할한다.

활용:

```text
문단 구조가 잘 정리된 일반 텍스트
간단한 문서
```

---

# 19. 재귀적 문자 분할

## RecursiveCharacterTextSplitter

LangChain에서 가장 일반적인 기본 splitter 중 하나이다.

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
```

일반적으로 큰 구분부터 시도한다.

```text
문단
↓ 실패하면
줄바꿈
↓ 실패하면
공백
↓ 실패하면
문자
```

즉:

```text
가능하면 자연스러운 문단 경계를 유지하면서
chunk_size 안에 들어오도록 계속 더 작은 기준으로 분할
```

한다.

활용:

```text
일반적인 RAG 문서
TXT
PDF 추출 텍스트
별도 구조가 없는 문서
```

### 최신성

2026 기준으로도 **좋은 기본 시작점**이다.

특별한 문서 구조가 없다면 먼저 이 방식으로 시작한 뒤 평가하는 것이 무난하다.

---

# 20. 토큰이란?

LLM은 텍스트를 글자 그대로 읽지 않는다.

먼저 Tokenizer가 텍스트를 token으로 나눈다.

```text
"나는 RAG를 공부한다"

↓ tokenizer

[token1, token2, token3, ...]
```

모델의 Context Window와 API 비용도 보통 token 기준이다.

따라서:

```text
문자 1000자
```

보다:

```text
500 tokens
```

처럼 모델 기준으로 분할해야 하는 경우가 있다.

---

# 21. Tokenizer란?

Tokenizer는:

```text
텍스트
↓
모델이 이해하는 token ID
```

로 변환하는 도구이다.

예:

```text
"Hello world"

↓ tokenizer

[9906, 1917]
```

토큰 분할 기준은 모델마다 다를 수 있다.

---

# 22. tiktoken

`tiktoken`은 OpenAI 계열 모델에서 많이 사용되는 tokenizer 라이브러리이다.

LangChain에서는:

```python
RecursiveCharacterTextSplitter.from_tiktoken_encoder(...)
```

같은 방식으로 사용할 수 있다.

예:

```python
splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    model_name="...",
    chunk_size=500,
    chunk_overlap=50
)
```

이 경우:

```text
분할 구조
→ Recursive Character

길이 계산
→ token 기준
```

으로 동작한다.

활용:

```text
OpenAI 모델 Context Window를 정확히 고려
토큰 비용 관리
```

---

# 23. TokenTextSplitter

직접 token을 기준으로 분할한다.

```python
from langchain_text_splitters import TokenTextSplitter

splitter = TokenTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
```

내부적으로 tokenizer로 encode한 뒤 token 묶음으로 자르고 다시 decode한다.

활용:

```text
Chunk 길이를 token 단위로 확실하게 제한
모델 최대 입력 길이를 엄격히 관리
```

---

# 24. spaCy

spaCy는 NLP 라이브러리이다.

단순 token 분할뿐 아니라:

```text
문장 경계
품사
개체명
문법 정보
```

등을 처리할 수 있다.

LangChain에는:

```python
from langchain_text_splitters import SpacyTextSplitter
```

가 있다.

주로 **문장 단위 분할**에 활용한다.

```text
문장 1.
문장 2.
문장 3.
```

활용:

```text
영어 문서
문장 구조를 보존하고 싶은 경우
```

---

# 25. NLTK

NLTK는 전통적인 Python NLP 라이브러리이다.

LangChain:

```python
from langchain_text_splitters import NLTKTextSplitter
```

주로 sentence tokenizer를 이용해 문장을 기준으로 나눈다.

활용:

```text
영문 자연어 문장 분할
교육 / 연구용 NLP
```

---

# 26. KoNLPy

KoNLPy는 한국어 NLP 라이브러리이다.

LangChain에는:

```python
from langchain_text_splitters import KonlpyTextSplitter
```

가 존재한다.

한국어는 영어처럼:

```text
공백
마침표
```

만으로 의미 단위가 항상 잘 나뉘지 않기 때문에 한국어 형태소 / 문장 처리 도구가 도움이 될 수 있다.

활용:

```text
한국어 문서
형태소 분석이 필요한 NLP
한국어 문장 기반 분할
```

---

# 27. Sentence Transformers

`SentenceTransformersTokenTextSplitter`는 Sentence Transformer 모델의 tokenizer 기준으로 분할한다.

```python
from langchain_text_splitters import SentenceTransformersTokenTextSplitter
```

특징:

```text
Embedding 모델 tokenizer 기준
```

즉 생성 LLM이 아니라 **Embedding 모델 입력 제한**에 맞춰 Chunk를 만들고 싶을 때 유용하다.

활용:

```text
Sentence Transformer 기반 Embedding
Embedding 모델 최대 token 길이를 맞출 때
```

---

# 28. Hugging Face Tokenizer

LangChain의 일반 TextSplitter는 Hugging Face tokenizer를 길이 계산 함수로 사용할 수 있다.

```python
splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
    tokenizer,
    chunk_size=500,
    chunk_overlap=50
)
```

장점:

```text
내가 실제 사용하는 Hugging Face 모델의 tokenizer 기준으로
Chunk 크기를 계산
```

활용:

```text
Llama
Qwen
Mistral
Hugging Face Embedding Model
```

등의 tokenizer 기준을 맞출 때 사용한다.

---

# 29. 토큰 기반 도구 비교

```text
tiktoken
→ OpenAI 계열 tokenizer 활용에 적합

TokenTextSplitter
→ token 묶음 자체를 기준으로 직접 분할

SentenceTransformersTokenTextSplitter
→ Sentence Transformer tokenizer 기준

Hugging Face tokenizer
→ 특정 HF 모델 tokenizer 기준

spaCy / NLTK / KoNLPy
→ 주로 자연어 문장 / 형태 구조를 활용한 분할
```

---

# 30. 의미 단위 분할

문자 수나 token 수가 아니라 **문장의 의미가 달라지는 지점**에서 Chunk를 나누는 방식이다.

예:

```text
문장 1: RAG는 외부 검색을 사용한다.
문장 2: Retriever는 관련 문서를 찾는다.
문장 3: 임베딩은 텍스트를 벡터로 변환한다.

---------------- 의미 변화 ----------------

문장 4: React는 UI 라이브러리다.
문장 5: useState는 상태를 관리한다.
```

결과:

```text
Chunk 1
→ RAG / Retriever / Embedding

Chunk 2
→ React / useState
```

---

## SemanticChunker

LangChain 생태계에는 `SemanticChunker`가 있다.

개념:

```text
문장 분할
↓
각 문장 / 문장 묶음 Embedding
↓
벡터 간 유사도 계산
↓
의미가 크게 바뀌는 지점 발견
↓
Chunk 분할
```

### LLM이 사용되는가?

기본 `SemanticChunker`는 **LLM을 호출하지 않는다.**

핵심은:

```text
LLM X

Embedding Model O
```

이다.

즉 의미 판단은 생성 LLM이 문장을 읽고 판단하는 것이 아니라:

```text
문장
↓
Embedding
↓
Vector
↓
Cosine Similarity
```

를 이용한다.

### 비용

문자 분할보다 비싸다.

```text
RecursiveCharacterTextSplitter
→ 문자열 연산 중심

SemanticChunker
→ Embedding 계산 필요
```

### 최신성

2026 기준 `SemanticChunker`는 여전히 **experimental 계열 성격**이 강하다.

따라서:

```text
기본 RAG
→ RecursiveCharacterTextSplitter

의미 경계가 매우 중요
→ Semantic Chunking 실험
```

정도로 접근하는 것이 좋다.

Semantic Chunking이 항상 더 좋은 것은 아니다.

반드시 retrieval 평가를 통해 비교하는 것이 좋다.

---

# 31. 코드 분할

코드는 일반 자연어와 구조가 다르다.

예:

```python
class UserService:

    def get_user():
        ...

    def delete_user():
        ...
```

이걸 문자 500자마다 자르면 함수 중간이 잘릴 수 있다.

그래서 코드에서는:

```text
class
function
method
block
```

등의 문법적 경계를 고려하는 것이 좋다.

LangChain에서는:

```python
RecursiveCharacterTextSplitter.from_language(...)
```

를 사용할 수 있다.

또 Python 전용:

```python
PythonCodeTextSplitter
```

도 있다.

예:

```python
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    Language
)

splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=500,
    chunk_overlap=50
)
```

활용:

```text
코드베이스 RAG
GitHub Repository QA
코드 검색
개발자 Agent
```

### 최신성

최근에는 React / Vue / Svelte 구조를 고려하는 `JSFrameworkTextSplitter`도 존재한다.

즉 코드 RAG에서는 단순 Character Split보다 **언어 구조 인식 splitter**를 고려하는 것이 좋다.

---

# 32. Markdown Header 분할

Markdown은 이미 의미 있는 구조를 가지고 있다.

```markdown
# RAG

## Retriever

내용...

## Embedding

내용...
```

따라서 단순 500자 기준보다 Header 구조를 이용하는 것이 자연스럽다.

```python
from langchain_text_splitters import MarkdownHeaderTextSplitter

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on
)
```

결과 `Document` metadata:

```python
{
    "Header 1": "RAG",
    "Header 2": "Retriever"
}
```

활용:

```text
기술 문서
README
개발 문서
Markdown Knowledge Base
```

### 장점

Header 정보를 metadata로 보존할 수 있다.

```text
검색 결과
↓
어느 섹션에서 나온 내용인지 알 수 있음
```

---

# 33. Markdown 구조 보존 최신 방식

현재 `langchain_text_splitters`에는:

```text
MarkdownHeaderTextSplitter
MarkdownTextSplitter
ExperimentalMarkdownSyntaxTextSplitter
```

등이 존재한다.

`ExperimentalMarkdownSyntaxTextSplitter`는:

```text
Header
Code Block
Horizontal Rule
Whitespace
```

등의 Markdown 문법 보존을 더 중요하게 다룬다.

아직 experimental이라는 점은 주의한다.

---

# 34. HTML Header 분할

HTML:

```html
<h1>RAG</h1>

<h2>Retriever</h2>
<p>...</p>

<h2>Embedding</h2>
<p>...</p>
```

Header를 기준으로 나눌 수 있다.

```python
from langchain_text_splitters import HTMLHeaderTextSplitter

splitter = HTMLHeaderTextSplitter(
    headers_to_split_on=[
        ("h1", "Header 1"),
        ("h2", "Header 2")
    ]
)
```

결과:

```text
Chunk
+
Header metadata
```

를 얻는다.

활용:

```text
웹 문서
공식 Documentation
HTML Knowledge Base
```

---

# 35. HTMLSemanticPreservingSplitter

2026 기준 `langchain_text_splitters`에는 단순 Header Splitter보다 더 발전된:

```text
HTMLSemanticPreservingSplitter
```

도 존재한다.

목적:

```text
HTML 구조 보존
표 / 미디어 / 요소 구조 유지
Header 기반 의미 구조 유지
```

Chunk가 너무 크면 내부적으로 재귀 분할을 적용할 수 있지만,
HTML 요소 자체를 가능한 한 깨지지 않게 보존하는 쪽에 초점이 있다.

복잡한 HTML 문서 RAG에서는 이런 구조 보존형 splitter를 고려할 수 있다.

---

# 36. JSON 분할

JSON은 계층 구조를 가진 데이터이다.

```json
{
  "company": {
    "name": "OpenAI",
    "products": {
      "chat": "...",
      "api": "..."
    }
  }
}
```

단순 문자 기준으로 자르면 JSON 구조가 깨질 수 있다.

그래서:

```python
from langchain_text_splitters import RecursiveJsonSplitter
```

를 사용한다.

예:

```python
splitter = RecursiveJsonSplitter(
    max_chunk_size=500
)

chunks = splitter.split_json(json_data)
```

특징:

```text
JSON 계층 구조를 최대한 유지
중첩 dictionary를 작은 JSON으로 분할
```

활용:

```text
API 응답
설정 파일
JSON Knowledge Base
대규모 JSON 데이터
```

---

# 37. JSON에 재귀적 문자 분할을 추가할 수 있는가?

가능하다.

다만 순서는 보통:

```text
JSON 구조 먼저 보존
↓
RecursiveJsonSplitter
↓
아직 너무 큰 Chunk
↓
RecursiveCharacterTextSplitter
```

가 자연스럽다.

예:

```python
json_chunks = json_splitter.split_json(data)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

final_chunks = []

for chunk in json_chunks:
    final_chunks.extend(
        text_splitter.split_text(str(chunk))
    )
```

하지만 이 방식은 두 번째 분할에서 JSON 구조가 일부 깨질 수 있다.

따라서:

```text
구조 보존이 중요
→ RecursiveJsonSplitter 위주

텍스트 검색 품질이 중요
→ 구조 분할 후 필요한 경우 재귀 문자 분할
```

처럼 선택해야 한다.

---

# 38. 구조 기반 분할 + 크기 기반 분할 조합

실무에서는 한 가지 Splitter만 쓰지 않을 수 있다.

예:

```text
Markdown
↓
Header 기준 분할
↓
각 Section
↓
RecursiveCharacterTextSplitter
↓
최종 Chunk
```

HTML:

```text
HTML
↓
Header / Semantic 구조 분할
↓
큰 Section만
↓
Recursive Character Split
```

JSON:

```text
JSON
↓
Recursive JSON Split
↓
큰 Chunk만
↓
Token / Character Split
```

이런 **2단계 Chunking**이 실용적이다.

---

# 39. Text Splitter 선택 기준

```text
일반 텍스트
→ RecursiveCharacterTextSplitter

정확한 LLM token 제한
→ TokenTextSplitter / tiktoken 기반

한국어 문장 처리
→ KoNLPy 고려

영문 문장 구조
→ spaCy / NLTK

Embedding 모델 tokenizer 기준
→ SentenceTransformers / Hugging Face tokenizer

주제가 바뀌는 의미 경계
→ SemanticChunker

코드
→ Language-aware / Code Splitter

Markdown
→ MarkdownHeaderTextSplitter

HTML
→ HTMLHeaderTextSplitter
   또는 HTMLSemanticPreservingSplitter

JSON
→ RecursiveJsonSplitter
```

---

# 40. 최신성 정리

> ⭐ 2026 기준 중요

## Text Splitter 패키지 분리

교재에서는 다음과 같은 예전 import를 볼 수 있다.

```python
from langchain.text_splitter import ...
```

현재는 Text Splitter들이 별도 패키지로 분리되어 있다.

```python
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TokenTextSplitter,
    MarkdownHeaderTextSplitter,
    HTMLHeaderTextSplitter,
    RecursiveJsonSplitter,
)
```

설치:

```bash
pip install langchain-text-splitters
```

즉 최신 코드에서는 `langchain_text_splitters`를 기준으로 보는 것이 좋다.

---

## Loader는 Integration 중심

많은 Loader는:

```python
langchain_community.document_loaders
```

에 위치한다.

예:

```python
PyPDFLoader
CSVLoader
DataFrameLoader
WebBaseLoader
DirectoryLoader
```

특정 기업 / 서비스 integration은 별도 패키지로 분리되는 흐름이 강하다.

예:

```text
Upstage
→ langchain_upstage
```

---

## 단순 분할보다 구조 보존이 중요해지는 추세

예전 교재:

```text
몇 글자마다 자를까?
```

중심이었다면,

최근 RAG에서는:

```text
Markdown Header
HTML 구조
Table
Code Function
JSON 계층
Document Layout
```

등을 최대한 보존한 뒤 크기 제한을 적용하는 전략을 많이 고려한다.

즉:

```text
문서 구조 기반 1차 분할
+
크기 기반 2차 분할
```

패턴이 중요하다.

---

## Semantic Chunking은 만능이 아니다

Semantic Chunking은 의미적으로 자연스러운 경계를 만들 수 있지만:

```text
Embedding 비용 발생
처리 시간 증가
결과 Chunk 크기 예측이 어려울 수 있음
```

단점이 있다.

또한 LangChain의 대표 `SemanticChunker`는 여전히 experimental 성격이 강하다.

따라서 무조건 Semantic Chunking을 쓰기보다:

```text
Recursive Character
vs
Structure-aware
vs
Semantic
```

를 실제 retrieval 평가로 비교해야 한다.

---

# 41. 가장 현실적인 시작 전략

처음 RAG를 만들 때:

```text
1. 문서에 맞는 Loader 선택
2. metadata 최대한 유지
3. RecursiveCharacterTextSplitter로 시작
4. 검색 품질 평가
```

그다음 문제가 보이면:

```text
문서 구조가 깨짐
→ Markdown / HTML / JSON / Code Splitter

문장 중간이 너무 많이 잘림
→ sentence 기반 분할

token 제한 문제
→ token 기반

주제 경계가 중요
→ Semantic Chunking 실험

표 / OCR / Layout 문제
→ Document AI Parser
```

로 발전시키는 것이 좋다.

---

# 42. 이 파트에서 기억할 핵심

```text
Document Loader
→ 원본 데이터를 읽는 단계

Document
→ page_content + metadata를 가진 공통 객체

Text Splitter
→ Document를 검색하기 좋은 Chunk로 나누는 단계

Chunk
→ 실제 Embedding / Vector Store 저장의 기본 단위
```

전체 흐름:

```text
PDF / HWP / CSV / WEB / JSON
↓
Loader / Parser
↓
Document
↓
Structure-aware Split
↓
Size / Token Split
↓
Chunk
↓
Embedding
↓
Vector Store
```

RAG의 검색 품질은 Embedding 모델만으로 결정되지 않는다.

**어떤 데이터를 어떻게 읽고, 어떤 단위로 나누었는지가 검색 품질에 큰 영향을 준다.**

---

# 43. 참고 문서

- LangChain Document  
  https://reference.langchain.com/python/langchain-core/documents/base/Document

- LangChain Community Document Loaders  
  https://reference.langchain.com/python/langchain-community/document-loaders

- LangChain Text Splitters  
  https://reference.langchain.com/python/langchain-text-splitters

- RecursiveCharacterTextSplitter  
  https://reference.langchain.com/python/langchain-text-splitters/character/RecursiveCharacterTextSplitter

- TokenTextSplitter  
  https://reference.langchain.com/python/langchain-text-splitters/base/TokenTextSplitter

- MarkdownHeaderTextSplitter  
  https://reference.langchain.com/python/langchain-text-splitters/markdown/MarkdownHeaderTextSplitter

- HTMLHeaderTextSplitter  
  https://reference.langchain.com/python/langchain-text-splitters/html/HTMLHeaderTextSplitter

- Upstage Document Parse Integration  
  https://reference.langchain.com/python/langchain-upstage/document_parse

- Unstructured Supported File Types  
  https://docs.unstructured.io/api-reference/supported-file-types
