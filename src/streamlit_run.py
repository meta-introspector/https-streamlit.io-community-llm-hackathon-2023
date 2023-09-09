import streamlit as st
import requests
import re
import streamlit.components.v1 as components
URL1="https://org-clarifai.streamlit.app/"

# Get the URL of the app to run from the query parameter or use a default value
url = st.experimental_get_query_params().get("url", URL1)
purl = st.experimental_get_query_params().get("purl", "http://localhost:8501/streamlit/run")

# Display a text input to let the user enter a new URL
new_url = st.text_input("Enter a new URL of a Streamlit app", value=url)
new_purl = st.text_input("Enter a new POST URL of a Streamlit app", value=purl)

# Set the new URL as a query parameter for the current app
#st.experimental_set_query_params(
#    url =new_url,
#    purl=new_purl)
#st.components.iframe(src=url, width=500, height=400)
#import streamlit as st

# embed streamlit docs in a streamlit app
components.iframe(new_url)

#Once the iframe is embedded, you can access the data from the embedded app using the `st.session_state` object. For example, if the embedded app has a variable called `data`, you can access it in your app as follows:

for d in st.session_state:
    data = st.session_state[d]

    st.write(d,data)

st.write(
    dict(
        url =new_url,
#        purl=new_purl
    ))
    
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
