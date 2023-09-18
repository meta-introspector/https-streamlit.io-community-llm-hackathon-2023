import streamlit as st
import zipfile
import urllib
import re
import os
app_args = dict()

# Define regex patterns to capture different parts
pattern_path = r'\./(?P<f3>[^:]+)/(?P<iid>[^:]+):'  # Matches everything between './' and ':'
pattern_raw = r'raw: "(?P<raw>[^"]+)"'  # Matches everything between 'raw: "' and '"'
pattern_payload = r'PAYLOAD:(?P<raw>[^"]+)"'  # Matches everything between 'raw: "' and '"'


def check(text):
    app_data={}
    # Search for patterns in the text
    match_path = re.search(pattern_path, text)
    match_raw = re.search(pattern_raw, text)
    match_payload = re.search(pattern_payload, text)

    # Check if matches are found
    path = ""
    raw_text = ""
    if match_path and match_raw:
        path = match_path.group(1) + match_path.group(2)
        raw_text = match_raw.group(1)
    elif match_path and match_payload:
        path = match_path.group(1) + match_path.group(2)
        raw_text = match_payload.group(1)
    else:
        if app_args["show-fails"]:
            st.error(text)
        
    #st.write("Path:", path)
    app_data["input_id"] = path
    app_data["text"] = text
    app_data["raw"] = raw_text
    #st.write("Raw Text:", raw_text)

    return app_data

def list_input(title, choices=[], key=None, choices_key=None, default_value=None):
    if not key:
        key = title

    if not choices_key:
        choices_key = key +"-choices"
    opt_index = 0

    if choices_key:
        if choices_key in oparams:
            for value in oparams[choices_key]:
                choices.append(toemoji(value))

    if key in params:
        default_value = params[key]

    if default_value in choices:
        opt_index = choices.index(default_value)

    selected_choice = st.selectbox(
        title,
        choices,
        key=key,
        index=opt_index,
    )

    return selected_choice
def get_page_size():
    return app_args['page_size']
def get_page_num():
    return app_args['page_num']


oparams = st.experimental_get_query_params()
params = {
    x: oparams[x][0]  for x in oparams
}
app_args.update(dict(    page_size = st.number_input("Page Size", min_value=1,key="page_size",
                                                     help="Use a number input widget to allow users to specify the page size. This will control how many items are displayed per page",
                                                     value=int(params.get("page_size", "100")))))

app_args.update(dict(page_num = st.number_input("Page Num",
                                                    min_value=0,
                                                    key="page_num",
                                                    help="Use a number input widget to allow users to specify the page num. This will control how many items are displayed per page",
                                value=int(params.get("page_num", "0")))))


app_args["base-url"] = st.text_input("base-url",
                                     key="base-url",
                                     value=params.get("base-url","https://org-clarifai-beta.streamlit.app"),
                                     help="for jwt")
app_args["show-fails"] = st.checkbox("show_fails",
                                     key="show-fails",
                                     help="Show failed regexes")
app_args.update(
        dict(
            app_id = st.text_input("app_id",
                                   help="id",
                                   value="Introspector-LLama2-Hackathon-Demo1"),
            target_url = st.text_input("target_url",
                                       key="target-url",
                                       value=params.get("target-url","https://org-clarifai-beta.streamlit.app"),
                                       help="for redirects"),
            jwt_url = st.text_input("jwt_url",
                                    key="jwt-url",
                                    value=params.get(
                                        "jwt-url",                                        
                                        "https://jwtjwt.streamlit.app/"
                                    ),
                                    help="where to send requests")
        ))

app_args.update(dict(
    concept_id = list_input(
        "Concept",
        ["python","Introspector"],
        key="concept_id",
        default_value="python")))

# Define the path to the ZIP file
zip_file_path = "vendor/data/index.zip"
target_file_name= "index.txt"
# Create a Streamlit app
st.title("Data View")

def get_base_url():
    return app_args['base-url']
def get_target_url():
    return app_args['target_url']

# User input for regex pattern
regex_pattern = st.text_input("Enter the regex pattern:")

import subprocess


# Check if the ZIP file exists
if not os.path.exists(zip_file_path):
    st.error("The ZIP file does not exist.")

    submodule_path = "vendor/data"

    # Create buttons to run submodule commands
    if st.button("Initialize Submodule"):
        try:
            result = subprocess.run(
                ["git", "submodule", "init", submodule_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            st.header("Submodule Initialization Output:")
            st.code(result.stdout)
            st.error(result.stderr)
        except Exception as e:
            st.error(f"Error: {e}")

    if st.button("Update Submodule"):
        try:
            result = subprocess.run(
                ["git", "submodule", "update", submodule_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            st.header("Submodule Update Output:")
            st.code(result.stdout)
            st.error(result.stderr)
        except Exception as e:
            st.error(f"Error: {e}")
            
else:
    # Display the list of contents when the ZIP file is available
    st.header("Contents of ZIP File")
    
    # Open the ZIP file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        # Get the list of files and directories inside the ZIP file
        file_list = zip_file.namelist()
        
        if not file_list:
            st.write("The ZIP file is empty.")
        else:
            # Display the list of contents
            for file_name in file_list:
                st.write(file_name)


        # Check if the target file exists in the ZIP archive
        if target_file_name not in zip_file.namelist():
            st.error(f"The file {target_file_name} does not exist in the ZIP archive.")
        else:
            # Create a button to run the regex
            #if st.button("Run Regex"):
            if True:
                try:
                    # Compile the regex pattern
                    compiled_pattern = re.compile(regex_pattern)

                    # Read and display the first 20 lines of the target file
                    with zip_file.open(target_file_name) as target_file:
                        file_contents = target_file.read().decode("utf-8").splitlines()
                        st.header(f"Contents of {target_file_name} :")
                        for line in file_contents[get_page_num()*get_page_size():(get_page_num()+1)*get_page_size()]:
                            #st.code(line)
                            
                            app_data = check(line)
                            input_id =""
                            if "input_id" in app_data:
                                input_id = app_data["input_id"]
                            else:
                                st.error(line)

                            # Match the pattern against the text
                            match = compiled_pattern.search(line)
                            if match:
                                # Otherwise, display the entire match
                                st.markdown(app_data["raw"])
                                st.write(f"Match: {match.group()}")
                                
                                    
                                # Get the current URL as a string
                                q= st.experimental_get_query_params()
                                q.update(app_args)
                                q.update(app_data)
                                q.update(match.groupdict())
                                q["line"] =""
                                q["raw"] =""
                                q["text"] =""
                                #st.dataframe(q)
                                encoded_query = urllib.parse.urlencode(q, doseq=True)
                                input_id = app_data["input_id"]
                                st.write(f"* [#{input_id}]({get_target_url()}/?{encoded_query})")


                except re.error as e:
                    st.error(f"Invalid regex pattern: {e}")
                    


# Display the text input
#st.header("Text Input")
#st.write(text_input)

# Display the regex pattern
#st.header("Regex Pattern")
#st.write(regex_pattern)

