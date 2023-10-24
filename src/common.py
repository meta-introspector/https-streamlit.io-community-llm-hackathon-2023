import urllib.parse
import streamlit as st

def get_link():
    oparams = st.experimental_get_query_params()
    params = {
        x: oparams[x][0]  for x in oparams
    }
    

    st.markdown(f"* share [input_link {encoded_query}]({base_url}/?{encoded_query})")
