def decide(data):
    if data:
        if not hasattr(data, '__iter__'):
            #st.write("The object is iterable.")
            if not isinstance(data, Iterable):
                #st.write("The object is iterable.")
                #else:
                name = ""
                if hasattr(data,"name"):
                    name = data.name()
                    
                data = [ "Just " + name + str(type(data)) + " debug "+ str(data) ]
                yield myselect(data)  # let the user select which ones
                return
            
            #for data1 in data:
            yield from myselect([data1 for data1 in data])  # let the user select which ones
