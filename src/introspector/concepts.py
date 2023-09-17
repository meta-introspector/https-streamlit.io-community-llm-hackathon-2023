import streamlit as st
from .modules.streamlitio.selector.list_input import list_input 
from .app_args import params,app_args
from .columns import col_concept

concept_choices = ["python", "streamlit", "clarifai"]  # Replace with your actual choices

def get_concept_id():
    return app_args['concept_id']

def get_concept():
    # Replace this part with your desired input logic
    app_args["mode"] = list_input(
        "Select a Concept",
        concept_choices,
        key="concept-choice",
        default_value=params.get("concept_id", "python")
    )

    get_concept_id()

