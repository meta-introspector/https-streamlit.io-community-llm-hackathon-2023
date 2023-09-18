import streamlit as st
import reveal_slides as rs

st.write("Input")
content_markdown = st.text_area("input", height=100)

response_dict = rs.slides(content_markdown)
st.write(response_dict)
