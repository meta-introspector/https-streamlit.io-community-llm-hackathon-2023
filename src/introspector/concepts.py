from .app_args import get_concept_id,params,app_args
from .columns import col_concept
import streamlit as st
def get_concept_id():
    return app_args['concept_id']
def get_inputs():
    with col_concept:
        app_args["concept_id"] = st.text_input(
            "Concept ID",
            key   =  "concept_id",
            help  = "Concept id to search for" ,
            value = params.get("concept_id","python")
        )
    return get_concept_id()
