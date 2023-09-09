import streamlit as st
import requests
import re
import streamlit.components.v1 as components
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation

URL1="https://org-clarifai.streamlit.app/?embed=true"
url = st.experimental_get_query_params().get("url", URL1)
new_url = st.text_input("Enter a new URL of a Streamlit app", value=url)
frame = components.iframe(new_url, width=500, height=400)

st.write(str(frame))
st.write(dir(frame))
#for x in dir(frame):
#    st.write(x,str(getattr(frame,x)))
#    st.write(x,str(help(getattr(frame,x))))

hs = st.text_input("Enter a new URL of a Streamlit app", value="'hi'")    
#streamlit_js_eval(hs)
st.write(f"IN {hs}")
hs1 = streamlit_js_eval(
    js_expressions=hs,
    key = 'SCR'
)
st.write(f"OUT {hs1}")


st.write(new_url)
    
# Run the app and get the output as a string
#output = requests.post(purl, data={"url": new_url}).text

# Display the output as it is
#st.write(output)

## Extract some data from the output using regular expressions
#data = {}
#data["title"] = re.search("<title>(.*?)</title>", output).group(1)
#data["headings"] = re.findall("<h[1-6]>(.*?)</h[1-6]>", output)
#data["links"] = re.findall("<a href=\"(.*?)\">(.*?)</a>", output)

# Display the data as a dictionary
#st.write(data)
# Set the new URL as a query parameter for the current app

#st.experimental_set_query_params(    url =new_url)
