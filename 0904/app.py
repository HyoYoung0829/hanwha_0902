import streamlit as st

home_page = st.Page("pages/home.py", title="홈", icon="🏠", default=True)

user_page = st.Page("pages/user.py", title="사용자", icon="👤")

pg = st.navigation([home_page, user_page])

pg.run()
