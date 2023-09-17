from .modes import get_inputs as get_mode
from .concepts import get_inputs as get_concept
from .get_inputs import get_ont_inputs
from .find_inputs import find_inputs

def observe():
    mode = get_mode() # create inputs needed
    concept = get_concept() # create inputs needed
    
    if mode == "concept-inputs":
        yield from find_inputs(concept)
    elif mode == "one-input":
        yield from get_one_input()
    else:
        st.write("something")
