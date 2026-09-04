import streamlit as st

st.set_page_config(page_title="백효영 포트폴리오", layout="wide")

st.title("안녕하세요!")
st.title('저는 프론트엔드 개발자 "백효영" 입니다.')

st.header("🌱 기술 스택")

skills = [
    ("Javascript", "js"),
    ("Typescript", "ts"),
    ("React", "react"),
    ("Next.js", "nextjs"),
    ("Zustand", "zustand"),
    ("Tailwind CSS", "tailwind"),
    ("Figma", "figma"),
    ("Supabase", "supabase"),
]

skill_html = '<div style="display:flex; gap:8px; flex-wrap:wrap; align-items:center;">'

for name, icon in skills:
    skill_html += f"""
<span style="
    display:inline-flex;
    align-items:center;
    justify-content:center;
    gap:6px;
    padding:6px 10px;
    border-radius:8px;
    background:#f0f2f6;
    color:#111;
    font-size:14px;
    font-weight:500;
">
<img
    src="https://skillicons.dev/icons?i={icon}"
    width="20"
    height="20"
/>
{name}
</span>
"""

skill_html += "</div>"

st.markdown(skill_html, unsafe_allow_html=True)

st.divider()

st.header("🔥 프로젝트")

st.markdown("""
- **두뇌 발달 미니게임 : 뇌하수체**
  - 2025.07 ~ 2025.08

- **공동편집 여행 플래너 : 플랜밍고**
  - 2025.08 ~ 2025.09

- **AI 법률 자문 및 판례 검색 : 바로**
  - 2025.09 ~ 2025.10

- **개인정보 걱정 없는 무료 모바일 초대장 : 인비아**
  - 2025.11 ~ 2026.07
""")

st.divider()

st.header("✌️ 교육 이수사항")

st.markdown("""
- **프로그래머스 데프코스 : 클라우드 기반 프론트엔드 엔지니어링**
  - 2025.05 ~ 2025.10

- **한화 내일 아카데미 : AI 에이전트**
  - 2026.09 ~ 2026.11
""")
