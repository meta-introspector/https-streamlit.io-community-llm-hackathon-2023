# from https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso
def doapply(data):
    for x in data:
        if isinstance(x,str):
            st.write("apply",x)
            yield x
        else:
            if hasattr(x,"apply"):
                yield from x.apply()
            else:
                st.write("do apply other",x)
                yield x

