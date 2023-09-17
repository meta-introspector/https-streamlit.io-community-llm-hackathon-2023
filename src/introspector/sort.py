
def sort(data):
    if isinstance(data, Iterable):
        if isinstance(data, types.GeneratorType):
            pass
        else:

            st.write("Sort Object is iterable",type(data).__name__,data)
        for x in data:
            yield x
    else:
        st.write("Sort Object not an iterable",data)
        yield data
