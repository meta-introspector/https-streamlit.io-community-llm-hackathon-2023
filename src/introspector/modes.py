import streamlit as st
# objerve /modeoc
from .columns import col1
from .app_args import get_mode,params,app_args

def get_inputs():
    with col1:
        app_args["mode"] = st.text_input("Mode",
                                         help="Mode to use",
                                         key="mode",value=params.get("mode","concept-inputs"))
    return get_mode()
# TODO 
class ConceptInputs():
    pass
class AllInputs():
    pass
class OneInputs():
    pass

modes = {
    "concept-inputs" : ConceptInputs(),
    "all-inputs": AllInputs(),
    "one-input": OneInputs(),
}        
