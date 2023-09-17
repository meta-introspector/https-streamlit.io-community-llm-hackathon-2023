from .modes import get_inputs as get_mode
from .concepts import get_inputs as get_concept
from .find_inputs import find_inputs

def observe():
    mode = get_mode() # create inputs needed
    concept = get_concept() # create inputs needed
    
    if mode == "concept-inputs":
        yield from find_inputs(concept)
    elif amode == "one-input":
        yield from get_inputs.get_inputs()
    else:
        st.write("something")
