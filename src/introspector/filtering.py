def filtering(data):
    if isinstance(data,str):
        yield data
        return
    if isinstance(data, Iterable):

        if isinstance(data, types.GeneratorType):
            pass
        else:            

            if "value" in data:
                v = data["value"]
                #st.write("VALUE",v)
            else:
                st.write("Filtering Object is iterable",type(data).__name__,data)
        for x in data:
            yield x
    else:
        st.write("Filtering Object not an iterable", data)
        yield data
