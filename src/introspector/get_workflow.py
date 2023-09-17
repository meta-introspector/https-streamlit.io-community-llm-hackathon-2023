
def get_workflow():
    if "workflow" in st.session_state:
        return st.session_state["workflow"]
    else:
        for x in  st.session_state:
            v = st.session_state[x]
            #st.write("DEBUG",x,v)
        return "default-workflow"
