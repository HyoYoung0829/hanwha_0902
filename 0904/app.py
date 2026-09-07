# streamlit 라우팅 페이지

import streamlit as st

# 페이지 객체 생성
# "pages/home.py" : 실행할 페이지 파일 경로
# title : 사이드바에 표시될 페이지 이름
# icon : 페이지 이름 앞에 표시할 아이콘 => 파비콘 같은 느낌인듯.
# default=True : 앱 실행 시 처음 보여줄 기본 페이지로 설정
home_page = st.Page("pages/home.py", title="홈", icon="🏠", default=True)

# 사용자 페이지 객체 생성
user_page = st.Page("pages/user.py", title="사용자", icon="👤")

# 위에서 만든 페이지들을 내비게이션 메뉴에 등록
# 리스트에 넣은 순서대로 메뉴에 표시됨
pg = st.navigation([home_page, user_page])

# 현재 선택된 페이지를 실행
pg.run()
