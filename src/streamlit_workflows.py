
workflows = {}
selected_workflows = None
def get_workflow():
    st.write("getwork",wf1)
    if "workflows" in st.session_state:
        return st.session_state["workflows"]
    else:
        return wf1

@st.cache_data
def get_workflow_gui():
    st.divider()
    global selected_workflows
    value = None
    #st.write("workflow params",params)
    #if "workflow" not in params:
        #params["workflow"] = "RakeItUpV3Using_emojis_instead_of_words_for0" # default                
    if "workflow" in params:        
        value=params.get("workflow",)
        #st.write("workflow arg value",value)
        if value is not None:
            if value :
                if value not in workflows:
                    workflows[value] = value
    ordered = sorted(list(workflows.keys()))
    
    aindex = 0
    
    if value is not None:
        #st.write("workflow value",value)
        #st.write("workflow order",ordered)
        aindex = ordered.index(value )
            
    if selected_workflows is None:
        if len(ordered) > 0:
            selected_workflows = st.selectbox("workflows",
                                              ordered,
                                              key="workflows",
                                              index=aindex,
                                              on_change=workflow_selected,
                                              kwargs={"workflow":value},
                                              help="choose which workflow to run.")
            #st.write("selected workflow",selected_workflows)
            #params["workflow2"] = selected_workflows
            #params["workflow8"] = selected_workflows
            return selected_workflows
    return selected_workflows
    
