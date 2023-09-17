###GUIDE 
def myselect(data):
    todo = []
    key = str(data)
    if isinstance(data,str):
        name = key + "button"
        if name not in seen:
            options = st.button(data,
                                key=name
                                )
            seen[name]=options
            #key + "button"
    else:
        for f in data:
            todo.append(f)
        if key not in seen:
            st.write("new data",data)
            options = st.multiselect(
                "Please select",todo,key=key)
            seen[key] = options
            st.write("You selected:", options)
            yield options
