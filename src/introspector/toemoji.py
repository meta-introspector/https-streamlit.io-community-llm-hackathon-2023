
def toemoji(data):
    ##decoratte the output
    if isinstance(data, types.GeneratorType):
        pass
    elif "value" in data:
        va = data["value"]
        if "url" in data:
            url = data["url"]
            aid = data["id"]
            name = va + "button"            
            if name in seen :
                return
            seen[name]=1
            #st.write("translate this into a structured emoji representation?",url)

            # Get the current URL as a string
            q= st.experimental_get_query_params()
            q.update(app_args)
            q["mode"] = "one-input"
            encoded_url = urllib.parse.urlencode({"url":url}, doseq=True)
            q["data_url"] = encoded_url
            q["input_id"] = aid
            encoded_query = urllib.parse.urlencode(q, doseq=True)
            st.markdown(f"* share [input_link {encoded_query}](/?{encoded_query})")
            options = st.button(va,
                            on_click=run_infer,
                            kwargs={
                                #"concept":selected_concept,
                                "value":va,
                                "url":url
                            },
                                key= va + "button",
                                help=str(q)
                            )
            seen[name]=options
        else:
            st.write("OTHER",data)
    else:
        pass
