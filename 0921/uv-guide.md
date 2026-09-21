# UV 학습 가이드 (npm 대응 버전)

프론트엔드 개발자(npm 경험자) 기준으로 UV를 npm과 비교하며 정리한 가이드.

---

## 1장. UV가 뭔지 + 설치

**한 줄 정의**: UV는 Rust로 만든 Python 패키지/프로젝트 관리 도구. pip + venv + pyenv + poetry를 하나로 합쳤다고 생각하면 됨.

### npm과 비교

Python 생태계는 지금까지 도구가 여러 개로 쪼개져 있었음:

| 역할 | Python (기존) | npm 세계에서는 |
|---|---|---|
| 패키지 설치 | pip | npm |
| 가상환경(격리) | venv / virtualenv | 필요 없음 (node_modules가 프로젝트별로 자동 격리) |
| Python 버전 관리 | pyenv | nvm |
| 프로젝트/의존성 관리 | poetry, pipenv 등 | package.json이 기본 내장 |
| 스크립트 실행 | 각자 알아서 | npm run |

프론트엔드는 npm 하나로 되는 일을 Python은 도구 3~4개를 조합해서 해왔음. UV는 이걸 한 바이너리로 통합했고, Rust로 짜여서 pip보다 체감상 10~100배 빠름.

### 설치

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 또는 Homebrew
brew install uv
```

설치 확인:
```bash
uv --version
```

### 전역 설치가 맞음

uv 자체는 전역에 까는 게 맞음. npm처럼 프로젝트마다 다시 설치하는 도구가 아니라, 시스템에 하나만 설치해두고 이후 모든 프로젝트에서 재사용.

- **uv 자체** = `nvm`이나 `npm` 본체 설치하듯이 전역에 한 번
- **uv로 설치하는 패키지들** (requests, django 등) = 프로젝트별 가상환경 안에 격리해서 설치

pip로 uv를 설치하는 것(`pip install uv`)도 가능은 하지만 권장하지 않음 — 공식 설치 스크립트가 버전 관리나 업데이트(`uv self update`)를 더 깔끔하게 처리해줌.

### 핵심 마인드셋

npm은 `node_modules`가 프로젝트 폴더 안에 자동으로 생기고 알아서 격리됨. Python은 원래 그게 기본이 아니라서 venv를 "수동으로" 만들어줘야 했음. UV는 이 부분을 npm처럼 **자동화**해줌 (4장에서 자세히 다룸).

---

## 2장. 프로젝트 시작하기

### npm이랑 비교

```bash
# npm
npm init -y

# uv
uv init
```

`uv init` 실행 시 자동으로 생성되는 것들:

```
my-project/
├── .python-version   # 이 프로젝트가 쓸 Python 버전 (nvm의 .nvmrc 같은 느낌)
├── .gitignore
├── README.md
├── pyproject.toml    # package.json 포지션
├── main.py           # 기본 진입 파일 (npm init엔 없는 것)
└── .git/             # git init까지 자동으로 됨
```

### pyproject.toml ↔ package.json

`package.json`:
```json
{
  "name": "my-project",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.0.0"
  }
}
```

`pyproject.toml`:
```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []
```

구조상 거의 1:1 대응. `dependencies` 배열도 개념 똑같음.

### 폴더 생성 방식

`uv init`은 폴더 이름을 인자로 주면 그 폴더까지 새로 만들어줌.

```bash
# 폴더 새로 만들면서 초기화
uv init my-project
cd my-project

# 이미 있는 폴더 안에서 초기화
mkdir my-project && cd my-project
uv init
# 또는
uv init .
```

| | npm | uv |
|---|---|---|
| 폴더 새로 만들면서 초기화 | `mkdir my-project && cd my-project && npm init -y` | `uv init my-project` (한 번에 됨) |
| 현재 폴더에서 초기화 | `npm init -y` | `uv init` |

---

## 3장. 패키지 설치/관리

### npm이랑 비교

```bash
# npm
npm install axios
npm install -D typescript
npm uninstall axios

# uv
uv add requests
uv add --dev pytest
uv remove requests
```

거의 1:1 대응. `-D`(devDependencies) 개념도 `--dev`로 그대로 있음.

### 설치하면 pyproject.toml이 자동으로 업데이트됨

```bash
uv add requests
```

`pyproject.toml`이 이렇게 바뀜:

```toml
[project]
dependencies = [
    "requests>=2.31.0",
]

[dependency-groups]
dev = []
```

### requirements.txt는 이제 어떻게 되나

원래 pip 방식:
```bash
pip install requests
pip freeze > requirements.txt
```

uv에서는 **`requirements.txt` 대신 `pyproject.toml` + `uv.lock`** 조합을 씀. `requirements.txt`는 레거시 호환용으로만 남아있음 (7장 마이그레이션 참고).

### lock 파일: uv.lock ↔ package-lock.json

`uv add`를 실행하면 `uv.lock`이 자동으로 같이 생기거나 갱신됨.

| | npm | uv |
|---|---|---|
| lock 파일 | `package-lock.json` | `uv.lock` |
| 역할 | 정확한 버전 고정, 재현 가능한 설치 | 동일 |
| 직접 수정? | 안 함 | 안 함 |
| 커밋해야 함? | O | O |

### 설치된 패키지 목록 보기

```bash
# npm
npm list

# uv
uv pip list
# 또는
uv tree   # npm list --all 처럼 트리 구조로 보여줌
```

### 명령어 매핑 정리 (install vs add/sync)

| 상황 | npm | uv |
|---|---|---|
| 패키지 하나 추가 | `npm install axios` | `uv add requests` |
| lock/설정 파일 보고 전체 설치 (예: git clone 직후) | `npm install` (인자 없이) | `uv sync` |
| 패키지 제거 | `npm uninstall axios` | `uv remove requests` |

npm은 `install` 하나가 "추가"와 "전체 설치" 두 역할을 다 하지만, uv는 이 두 개를 `add`(추가)와 `sync`(전체 설치/동기화)로 명확히 나눔. `git clone` 받은 프로젝트 세팅할 때는 `uv add`가 아니라 `uv sync`를 써야 함.

---

## 4장. 가상환경 개념

### 왜 Python은 격리가 필요한가

npm 구조:
```
project-a/
└── node_modules/   ← 여기만 봄, 프로젝트 로컬

project-b/
└── node_modules/   ← 완전히 별개
```

각 프로젝트 폴더 안에 `node_modules`가 있어서 자동으로 격리됨.

Python은 원래 이렇게 생기지 않았음. `pip install requests`를 그냥 실행하면 시스템 전체(또는 사용자 전역)에 깔리는 게 기본값이었음. 그래서:

```
project-a가 requests 2.0을 원함
project-b가 requests 3.0을 원함
→ 시스템에 하나만 깔리니까 충돌남
```

이 문제를 해결하려고 만든 게 **venv(가상환경)** — "이 프로젝트 전용 Python 설치 공간"을 폴더 하나로 만들어서 node_modules처럼 프로젝트별로 격리.

### 비교표

| | npm | Python (원래 pip 방식) | uv |
|---|---|---|---|
| 격리 단위 | `node_modules/` | `.venv/` (수동 생성 필요) | `.venv/` (자동 생성) |
| 만드는 명령어 | 필요 없음 (자동) | `python -m venv .venv` + `source .venv/bin/activate` | 필요 없음 (자동) |
| 실행 전 활성화 | 필요 없음 | 매번 `activate` 해야 함 | 필요 없음 |

`.venv`가 사실 npm의 `node_modules`와 같은 역할을 함. 옛날 pip 방식은 이걸 사람이 직접 만들고 켜고 꺼야 했음.

### uv는 이걸 어떻게 자동화하나

`uv add`나 `uv sync`를 실행하면:

```
my-project/
├── .venv/          ← uv가 알아서 만들어줌
├── pyproject.toml
└── uv.lock
```

`.venv`가 자동으로 생기고, activate를 수동으로 할 필요가 없음. `uv run`(5장)이 알아서 이 `.venv`를 찾아서 씀.

---

## 5장. 스크립트/명령어 실행

### npm이랑 비교

```bash
# npm
npm run dev
npm run build
node index.js

# uv
uv run python main.py
uv run pytest
```

### activate가 왜 필요 없나

`activate`가 실제로 하는 일은 **현재 쉘 세션의 환경변수(PATH)를 바꾸는 것**. `.venv/bin/python`을 먼저 찾게 만드는 방식.

```bash
source .venv/bin/activate   # 이 쉘 세션의 PATH를 오염시킴
python main.py               # 이제 python이 .venv 걸 가리킴
deactivate                   # PATH 원상복구
```

문제는 이게 **쉘 세션 전체**에 영향을 준다는 것. 한 번 activate 하면 그 터미널 탭에서 계속 유지되기 때문에 다른 프로젝트로 넘어가기 전에 수동으로 deactivate 해줘야 했음.

`uv run`은 현재 쉘의 환경을 건드리지 않음. 그 명령어 한 번만 `.venv`를 가리키는 환경으로 감싸서 실행하고, 끝나면 프로세스가 그냥 종료됨.

| | 기존 방식 | uv run |
|---|---|---|
| 방식 | 쉘 전체의 스위치를 켰다 껐다 | 명령어 하나하나를 격리된 상자에 넣어서 실행 |
| 지속시간 | activate~deactivate 사이 계속 유지 | 그 명령어 한 번 실행되는 동안만 |
| deactivate 필요? | O (안 하면 다음 프로젝트에서 꼬임) | X (쉘 상태를 안 건드려서 꼬일 일이 없음) |

```bash
cd project-a
uv run python main.py    # 실행되고 끝

cd ../project-b
uv run pytest             # 얘도 알아서 project-b의 .venv로 실행됨
```

결과적으로 npm과 동일한 감각: `node_modules`를 프로젝트 로컬로 자동 찾아 쓰듯, uv도 매 명령어마다 "지금 이 폴더의 `.venv`가 뭐지"를 알아서 판단해서 실행함.

### package.json의 "scripts" 필드는?

Python/uv 쪽엔 동일한 "scripts" 개념이 `pyproject.toml`에 있음:

```toml
[project.scripts]
start = "my_project:main"
```

근데 이건 주로 **패키지를 CLI 도구로 배포할 때** 쓰는 용도라 npm scripts처럼 "개발용 단축 명령어" 목적으로는 잘 안 씀. 개발 중엔 그냥:

```bash
uv run python main.py
uv run pytest
uv run ruff check .
```

이렇게 `uv run <명령어>` 형태로 직접 실행하는 게 일반적.

### 비교표

| | npm | uv |
|---|---|---|
| 스크립트 실행 | `npm run dev` (package.json에 정의 필요) | `uv run <아무 명령어>` (정의 없이 바로) |
| 임시 실행 | `npx <패키지>` | `uvx <패키지>` |

`npx`에 대응하는 게 `uvx` — 설치 안 하고 1회성으로 도구 실행할 때 씀 (예: `uvx ruff check .`).

---

## 6장. Python 버전 관리

### npm이랑 비교

```bash
# nvm
nvm install 18
nvm use 18
nvm list

# uv
uv python install 3.12
uv python pin 3.12
uv python list
```

거의 1:1 매핑.

### uv python install ↔ nvm install

```bash
uv python install 3.12
```

uv가 Python 3.12를 다운받아서 uv 전용 공간에 설치. 시스템 Python과 별개로 관리되니까 여러 버전 깔아놔도 서로 안 꼬임.

### uv python pin ↔ .nvmrc 만들기

```bash
uv python pin 3.12
```

프로젝트 루트에 `.python-version` 파일이 생기거나 갱신됨:

```
3.12
```

`.nvmrc`에 `18.20.0` 적어두는 것과 완전히 같은 역할. 이 파일이 있으면 `uv run`이나 `uv sync` 할 때 uv가 자동으로 인식함.

### 비교표

| | nvm | uv |
|---|---|---|
| 버전 설치 | `nvm install 18` | `uv python install 3.12` |
| 프로젝트에 버전 고정 | `.nvmrc` 파일 (수동 작성) | `.python-version` 파일 (`uv python pin`으로 자동 생성) |
| 설치된 버전 목록 | `nvm list` | `uv python list` |
| 자동 인식 | `nvm use` 수동 실행 필요 (또는 쉘 훅 설정) | `uv run`/`uv sync` 할 때 자동으로 `.python-version` 읽음 |

nvm은 `.nvmrc`가 있어도 `nvm use`를 직접 쳐주거나 별도 쉘 설정이 필요함. uv는 별도 설정 없이 `uv run`, `uv sync`가 기본적으로 `.python-version`을 읽어서 그 버전을 씀.

### Python 자체가 시스템에 없어도 되나

`uv python install`을 안 해도 `uv run` 시점에 `.python-version`에 명시된 버전이 없으면 uv가 알아서 다운받아 설치해줌. 이론상 pyenv/시스템 Python 없이 uv 하나만 깔려있어도 프로젝트 실행이 가능.

---

## 7장. 기존 requirements.txt 프로젝트 마이그레이션

이미 pip + requirements.txt로 짜여진 프로젝트를 uv로 옮기는 상황. 실무에서 제일 자주 마주치는 케이스.

### 시나리오: 기존 프로젝트 구조

```
old-project/
├── requirements.txt
├── requirements-dev.txt   (있을 수도 있음)
└── main.py
```

`requirements.txt` 예시:
```
requests==2.31.0
pydantic>=2.0
```

### 방법 1: uv init 후 requirements.txt를 add로 흡수

```bash
cd old-project
uv init .
uv add -r requirements.txt
```

`uv add -r requirements.txt`가 핵심. 이 명령어가:

1. `requirements.txt`의 패키지들을 읽어서
2. `pyproject.toml`의 `dependencies`에 등록하고
3. `.venv` 만들어서 실제로 설치까지 함
4. `uv.lock` 생성

dev 쪽도 있으면:
```bash
uv add -r requirements-dev.txt --dev
```

### 방법 2: requirements.txt 형식을 그대로 유지하고 싶을 때

팀 전체가 아직 uv로 전환 안 했거나, CI/CD가 `requirements.txt`를 기대하는 상황이면 `pyproject.toml`을 안 쓰고 uv를 더 빠른 pip 대체제로만 쓸 수도 있음:

```bash
# pip install -r requirements.txt 대신
uv pip install -r requirements.txt

# pip freeze 대신
uv pip freeze > requirements.txt
```

기존 pip 워크플로우 명령어를 그대로 쓰되 속도만 빠르게 가져가는 방식. 과도기에 유용함.

### 최종적으로 어느 방식을 쓸지

| 상황 | 추천 |
|---|---|
| 혼자 하는 프로젝트, 완전히 uv로 전환 | 방법 1 (`uv add -r`) |
| 팀원들이 아직 pip 쓰는 중, 점진적 전환 | 방법 2 (`uv pip`) |
| CI가 requirements.txt를 요구함 | `uv export`로 `pyproject.toml` → `requirements.txt` 역변환 |

### uv export (pyproject.toml → requirements.txt로 내보내기)

```bash
uv export -o requirements.txt
```

`uv.lock` 기준으로 `requirements.txt`를 만들어줌. 배포 환경이 uv를 지원 안 하고 pip만 쓸 수 있는 경우(일부 레거시 서버, Docker 베이스 이미지 제약 등) 대비용으로 씀.
