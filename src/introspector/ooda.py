from .observe import observe
from .orient import orient
from .decide import decide
from .act import act

def ooda():
    for sample in observe():
        samples = []
        for oriented in orient(sample):
            #st.write("orient",oriented)
            samples.append(oriented)
        for decision in decide(samples):
            yield from act(decision)
