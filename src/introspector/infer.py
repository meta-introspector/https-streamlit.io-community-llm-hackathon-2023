
def run_infer(value, url):
    #st.write("infer",value, url)

    #st.write("selected",wf)
    workflow = get_workflow()
    #st.write("workflow",workflow)
    data_url = url

    ci = get_concept_id()

    concepts=[workflow]
    if ci :
        concepts.append(ci)

    try:
        ret = call_api.call_workflow(stub, user_metadata, get_userDataObject(), workflow, data_url, concepts)
        #st.write(ret)
    except Exception as e:
        st.write("ERROR",e)
        raise e
