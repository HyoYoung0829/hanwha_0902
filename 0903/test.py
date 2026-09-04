import streamlit as st
import streamlit.components.v1 as components
import left
import right

st.set_page_config(layout="wide")

components.iframe("https://www.invia.co.kr", height=900)

col1, col2 = st.columns(2)

with col1:
    left.render()

with col2:
    right.render()
