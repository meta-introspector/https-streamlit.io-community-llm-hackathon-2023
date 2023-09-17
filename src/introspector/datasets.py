def datasets(app):
    if app.name in app_datasets:
        st.write ("DEBUG1",app.name)
        for name in app_datasets[app.name]:
            st.write ("DEBUG2",app.name, "in", app_datasets)
            yield name
    else:
        #st.write ("DEBUG",app.name, "not in", app_datasets)
        pass
