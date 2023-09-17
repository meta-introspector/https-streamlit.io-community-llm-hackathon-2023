#@st.cache_resource
def apps():
    # list the apps we have access to

    for app in our_apps:
        yield app
        all_apps.append(app.id)
        try:
            wf = app.list_workflows()
            for w in wf:
                #st.write({  "workflow":w.id            })
                add_workflows(w)
        except Exception as e:
            st.code(e)
            raise e
            
    #global selected_app
    
    #get_workflow_gui()

    #if selected_app is None:
    #    selected_app = st.selectbox("apps",all_apps)
        
