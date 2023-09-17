import streamlit as st

# globals
app_args = {}
oparams = st.experimental_get_query_params()
params = {
    x: oparams[x][0]  for x in oparams
}

def get_mode():
    return app_args['mode']

def get_concept_id():
    return app_args['concept_id']

def get_input_id():
    return app_args['input_id']
    
def get_last_id():
    return app_args['last_id']

def get_app_id():
    return app_args['app_id']

def get_page_size():
    return app_args['page_size']
