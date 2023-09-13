import os
from collections.abc import Iterable
#xfrom streaamlit.server.server import Server
#from streamlit_server_state import server_state, server_state_lock
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
import streamlit as st
import types
import call_api
import emojis
import requests
import urllib.parse        
from clarifai.client.user import User
from clarifai_grpc.grpc.api import resources_pb2
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

wf1 = None
def workflow_selected(workflow):
    #globals wf1
    st.write("Workflow selected",workflow)
    wf1 = workflow
    

# Create widgets for each parameter
oparams = st.experimental_get_query_params()
params = {
    x: oparams[x][0]  for x in oparams
}
#st.write(params)

workflows = {}
selected_workflows = None
def get_workflow():
    st.write("getwork",wf1)
    if "workflows" in st.session_state:
        return st.session_state["workflows"]
    else:
        return wf1
def get_workflow_gui():
    global selected_workflows
    value = None
    #st.write("workflow params",params)
    if "workflow" not in params:
        params["workflow"] = "RakeItUpV3Using_emojis_instead_of_words_for0" # default                
    if "workflow" in params:        
        value=params.get("workflow",)
        #st.write("workflow arg value",value)
        if value is not None:
            if value :
                if value not in workflows:
                    workflows[value] = value
    ordered = sorted(list(workflows.keys()))
    
    aindex = 0
    
    if value is not None:
        #st.write("workflow value",value)
        #st.write("workflow order",ordered)
        aindex = ordered.index(value )
            
    if selected_workflows is None:
        if len(ordered) > 0:
            selected_workflows = st.selectbox("workflows",
                                              ordered,
                                              key="workflows",
                                              index=aindex,
                                              on_change=workflow_selected,
                                              kwargs={"workflow":value},
                                              help="choose which workflow to run.")
            #st.write("selected workflow",selected_workflows)
            #params["workflow2"] = selected_workflows
            #params["workflow8"] = selected_workflows
            return selected_workflows
    return selected_workflows
    
app_args = dict(
    concept_id = st.text_input("ConceptID", help="Concept id to search for" , value ="python"),
    # number_input(label, min_value=None, max_value=None, value=, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False, label_visibility="visible")
    page_size = st.number_input("Page Size", min_value=1,
                                help="Use a number input widget to allow users to specify the page size. This will control how many items are displayed per page",
                                value=int(params.get("page_size", "10"))),
    last_id = st.text_input("Last Id", value=params.get("last_id", ""),
                            help= "Last Id as a starting token, enter or select the token."
                                   ),
    workflow = None,
    num_runs = st.number_input("Number of Runs",
                               min_value=1,
                               value=int(params.get("num_runs", 1)),
                               help="how many times they want to run the selected workflow."
                               ),
    output_location = st.text_input("Output Location", value=params.get("output_location", ""),
                                    help="specify where to store the output, whether it's a file path or a cloud storage location."
                                    ),
    summarize_output = st.checkbox("Summarize Output",
                                   value=params.get("summarize_output", False),                                   
                                   help = "toggle summarization on or off. When summarization is enabled, provide a summary of the outputs; otherwise, display detailed outputs."  ),
    )

def get_concept_id():
    return app_args['concept_id']

def add_workflows(w):
    global workflows
    workflows[w.id] = w
    
def get_last_id():
    return app_args['last_id']

def get_page_size():
    return app_args['page_size']

# Display the result based on parameters


PAT = st.secrets["CLARIFAI_PAT"]
USER_ID =st.secrets["clarifai_user_id"]
channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)
metadata = (('authorization', 'Key ' + PAT),)

userDataObject= None
def get_userDataObject():
    global userDataObject
    if userDataObject is None:
        userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=app_id)
    return userDataObject        
    
# globals
seen = {}
our_apps= {}
app_datasets = {}
os.environ["CLARIFAI_PAT"] = st.secrets["CLARIFAI_PAT"]
client = User(user_id=st.secrets["clarifai_user_id"])

# from https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True


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


def act(data):
    if not data:
        return
    for data1 in data:
        yield from doapply(data1)  # apply those changes to the api


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


m  = emojis.Emojis()
concepts1 = {}
def get_concepts():
    #return self.get_dataset_names_with_prefix()
    m  = emojis.Emojis()
    dataset_names = {}

    for x in m.process():
        #print(x)
        #{'combine': ['Create prompt model that will ', "define the <generator object Emojis.prompt_model at 0x7fc73600d770> with args {'emoji': '📥🔗📜'} using example :'''{data.text.raw}'''"]}
        if "combine" in x:
            c1 = x["combine"]
            x1 = c1[0]
            x2 = c1[1]
            #print("DEBUG",c1, x1, x2)

            if x1 not in concepts1:
                orig = x1
                concepts1[x1] = 1
                x1 = x1.strip()
                x1 = x1.replace(" ","_")
                x1 = x1.replace("__","_")
                #print("CONCEPT",x1)
                #print("ORIG",orig)
                if len(orig)<3:
                    raise Exception("nope")
                #
                for i,p in enumerate([
                        f"The concept of {orig} and its relationship to the concepts contained in '''{{data.text.raw}}'''",
                        f"The concept of {orig} in '''{{data.text.raw}}'''",
                        f"The concept of {orig} in consideration of the special case of {x1} in '''{{data.text.raw}}'''",
                        f"The concept of {orig} and {x1} in '''{{data.text.raw}}'''",
                        f"Relate {orig} to '''{{data.text.raw}}'''",                        
                ]):
                    #print("DEBUG!ORIG", orig)
                    #print("DEBUG!",  x1)
                    #print("DEBUG!", str(i))
                    #print("DEBUG!P", str(p))

                    dataset_names[x1 +str(i)] = dict(
                        prompt=p,
                        orig=orig,
                        i=i,
                        x1=x1,
                        p=p,
                        source=x,
                        emojis=m,
                        )

            #dataset_names[x] = x
    return dataset_names

concept_list = []

for x in get_concepts():
    #st.write(x)
    concept_list.append(x)
#selected_concept = st.selectbox("concepts",concept_list)

def run_infer(value, url):
    st.write("infer",value, url)

    #st.write("selected",wf)
    workflow = get_workflow()
    data_url = url
    st.write("selected",selected_app)
    ci = get_concept_id()

    concepts=[workflow]
    if ci :
        concepts.append(ci)

    try:
        ret = call_api.call_workflow(stub, metadata, get_userDataObject(), workflow, data_url, concepts)
        st.write(ret)
    except Exception as e:
        st.write(e)


def toemoji(data):
    
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
            q["data_url"] = url
            q["input_id"] = aid
            #q["1workflow"] = get_workflow()

            if "workflows" in st.session_state:
                q["workflow"] = st.session_state["workflows"]

            # generic
            #for x in st.session_state:
            #    q[f"st_{x}"] = str(st.session_state[x])                
                #q[f"st_{x}"] = str(st.session_state[x])
                
            #q["input_name"] = name
            #q["input_value"] = va # skip this for shortness


            encoded_query = urllib.parse.urlencode(q, doseq=True)
            #st.write(encoded_query)            
            
            st.markdown(f"* share [input_link {encoded_query}](/?{encoded_query})")

            #for session_info in Server.get_current()._session_info_by_id.values():

            #st.write(parsed_url)
            # Replace the query part of the URL with the new string
            #new_url = parsed_url._replace(query=encoded_query).geturl()
            # Write the new URL as a link
            #st.write(f"[New URL]", new_url)


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
        #st.write()
        pass


    # 


def summarize(data):

    # lets see if we can use emojis to summarize.
    toemoji(data)
    
    #if isinstance(data, generato):
    if isinstance(data, Iterable):
        if isinstance(data, types.GeneratorType):
            pass
        else:
            st.write("Sum Object is iterable", type(data).__name__, data, )
        for x in data:
            yield x
    else:
        st.write("Sum Object not an iterable")
        yield data


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
        
def orient(data):
    toemoji(data)
    yield from summarize(
        sort(
            filtering(data)))  # show a summary of the data
all_apps = []
selected_app = None 
def apps():
    # list the apps we have access to

    for app in our_apps:
        yield app
        all_apps.append(app.id)
        wf = app.list_workflows()
        for w in wf:
            #st.write({  "workflow":w.id            })
            add_workflows(w)
    
    global selected_app
    
    get_workflow_gui()

    if selected_app is None:
        selected_app = st.selectbox("apps",all_apps)
        
            
def datasets(app):
    if app.name in app_datasets:
        st.write ("DEBUG1",app.name)
        for name in app_datasets[app.name]:
            st.write ("DEBUG2",app.name, "in", app_datasets)
            yield name
    else:
        #st.write ("DEBUG",app.name, "not in", app_datasets)
        pass

def inputs(dataset):
    for x in ("inputa","inputb"):
        yield dataset + x
app_id = None


def find_inputs(concept_id):
    #st.write("search for concepts",concept_id)
    #st.write("user data",userDataObject)
    #st.write("stub",stub)
    post_annotations_searches_response = stub.PostAnnotationsSearches(
        service_pb2.PostAnnotationsSearchesRequest(
            user_app_id=get_userDataObject(),  
            searches = [
                resources_pb2.Search(
                    query=resources_pb2.Query(
                        filters=[
                            resources_pb2.Filter(
                                annotation=resources_pb2.Annotation(
                                    data=resources_pb2.Data(
                                        concepts=[  # You can search by multiple concepts
                                            resources_pb2.Concept(
                                                id=concept_id,  # You could search by concept Name as well
                                                value=1  # Value of 0 will search for images that don't have the concept
                                            )
                                        ]
                                    )
                                )
                        )
                        ]
                    )
                )
            ]
        ),
        metadata=metadata
    )
    
    if post_annotations_searches_response.status.code != status_code_pb2.SUCCESS:
        st.write("Post searches failed, status: " + post_annotations_searches_response.status.description)

        #st.write("Search result:")
    for hit in post_annotations_searches_response.hits:
        #st.write("\tScore %.2f for annotation: %s off input: %s" % (hit.score, hit.annotation.id, hit.input.id))
        #yield hit
        value  = str(hit)
        ##
        #         0:"ByteSize"
        # 1:"Clear"
        # 2:"ClearExtension"
        # 3:"ClearField"
        # 4:"CopyFrom"
        # 5:"DESCRIPTOR"
        # 6:"DiscardUnknownFields"
        # 7:"Extensions"
        # 8:"FindInitializationErrors"
        # 9:"FromString"
        # 10:"HasExtension"
        # 11:"HasField"
        # 12:"IsInitialized"
        # 13:"ListFields"
        # 14:"MergeFrom"
        # 15:"MergeFromString"
        # 16:"ParseFromString"
        # 17:"RegisterExtension"
        # 18:"SerializePartialToString"
        # 19:"SerializeToString"
        # 20:"SetInParent"
        # 21:"UnknownFields"
        # 22:"WhichOneof"
        # 23:"_CheckCalledFromGeneratedFile"
        # 24:"_ListFieldsItemKey"
        # yield({
        #     "type": "hit",
        #     #"dir": dir(hit),
        #     "ListFields": hit.ListFields(),
        #     #"url": hit.data.text.url,
        #     "value": value})

        
        for x in hit.ListFields():
            
            # yield({
            #     "type": "hitf",
            #     "dir": dir(x),
            #     #"count": x.count(),
            #     #"index": x.index(),
            #     "value": str(x)
            # })

            for y in x:
                if isinstance(y, resources_pb2.Input):
                    input_object = y 
                    data2 =  requests.get(input_object.data.text.url)
                    value =   data2.text
                    yield({
                        "type": "input",
                        "id": input_object.id,
                        "url": input_object.data.text.url,
                        "value":             value})
                    
                # else:
                #     yield({
                #         "type": "hitfy",
                #         "dir": dir(y),
                #         "type2": type(y),                    
                #         "value": str(y)
                #     })
    
def unassigned_inputs(data):
    
    global app_id
    if selected_app:
        app_id = selected_app
    
    page_size = get_page_size()
    if page_size is '':
        page_size = 10
    else:
        page_size = int(page_size)

    kwargs={}
    st = get_last_id()
    if str:
        kwargs["last_id"]=st

    stream_inputs_response = stub.StreamInputs(
        service_pb2.StreamInputsRequest(
            user_app_id=get_userDataObject(),
            per_page=int(page_size),
            **kwargs
        ),
        metadata=metadata
    )
    if stream_inputs_response.status.code != status_code_pb2.SUCCESS:
        yield({"status":stream_inputs_response.status})
        raise Exception("Stream inputs failed, status: " + stream_inputs_response.status.description)
    for input_object in stream_inputs_response.inputs:
        data2 =  requests.get(input_object.data.text.url)
        value =   data2.text
        yield({
            "type": "input",
            #"res": data2.resu
            "id": input_object.id,
            "url": input_object.data.text.url,
            "value":             value})

def observe():
    wf = get_workflow_gui()
    for app in apps():
        global app_id
        app_id = app.id
        st.write("App",app.name)

        # yield from unassigned_inputs(app)
        for dataset in datasets(app):
            st.write("Dataset",dataset)
            for input in inputs(dataset):
                yield {"dataset": [ app , dataset, input ]}

        #just do the inputs last ...
        yield from find_inputs(get_concept_id())

def ooda():
    for sample in observe():
        samples = []
        for oriented in orient(sample):
            #st.write("orient",oriented)
            samples.append(oriented)
        for decision in decide(samples):
            yield from act(decision)


# taken from https://gist.githubusercontent.com/iankelk/7e46c9935442ba01853b1689ff4a5038/raw/a261f99e6dd9cef6cc3d9ee04648df40232072d9/C-everything.py
def load_pat():
    if "CLARIFAI_PAT" not in st.secrets:
        st.error("You need to set the CLARIFAI_PAT in the secrets.")
        st.stop()
    return st.secrets.CLARIFAI_PAT


def get_default_models():
    if "DEFAULT_MODELS" not in st.secrets:
        st.error("You need to set the default models in the secrets.")
        st.stop()
    models_list = [x.strip() for x in st.secrets.DEFAULT_MODELS.split(",")]
    models_map = {}
    select_map = {}
    for i in range(len(models_list)):
        m = models_list[i]
        id, rem = m.split(":")
        author, app = rem.split(";")
        models_map[id] = {}
        models_map[id]["author"] = author
        models_map[id]["app"] = app
        select_map[id + " : " + author] = id
    return models_map, select_map



def main():
    global our_apps
    #st.set_page_config(layout="wide")

    our_apps = client.list_apps()



    #if check_password():
    if True: # skip password for now
        for x in ooda():
            if isinstance(x,str):
                st.write("str",x)
            else:
                if hasattr(x,"apply"):
                    for x in  x.apply():
                        st.write("app",x)
                    else:
                        st.write("other",x)
                        
    models = {}
    dataset_index = {}

    for app in our_apps:
        datasets = app.list_datasets()
        for ds in datasets:
            name = ds.dataset_info.id
            if app not in app_datasets:
                app_datasets[app.name]={}
            if name not in app_datasets[app.name]:
                app_datasets[app.name][name] = ds
        
            dataset_index[name] = ds
    for model_name in models:
        idn = "cf_dataset_" + model_name.lower()
        if idn not in dataset_index:
            dataset = app.create_dataset(dataset_id=idn)
        else:
            models[model_name].set_dataset(dataset_index[idn])
        models[model_name].sync()

#### experimental args
# Retrieve URL parameters


# defaults to be populated by apps
args = {
    # "page_size": 10,
    # "last_id": "",
    # "concept_id": "python",
    # "workflow":"RakeItUpV3a_self_referential_tensor_containing4",
    # "num_runs": 1,
    # "output_location": "",
    # "summarize_output": False
}


def get_args():
    params = st.experimental_get_query_params()
    
#     page_size = int(params.get("page_size", 10))
#     last_id = params.get("last_id", "")

#     num_runs = int(params.get("num_runs", 1))
#     output_location = params.get("output_location", "")
#     summarize_output = params.get("summarize_output", False)    
# # Create widgets for each parameter
# page_size = st.number_input("Page Size", min_value=1, value=page_size)

# last_id = st.text_input("Starting Token", value=last_id)
# num_runs = st.number_input("Number of Runs", min_value=1, value=num_runs)
# output_location = st.text_input("Output Location", value=output_location)
# summarize_output = st.checkbox("Summarize Output", value=summarize_output)


# Function to apply changes
def apply_changes(**args):
    # Update URL with current parameter values
    st.experimental_set_query_params(**args  )

# Add an "Apply" button
st.button("Apply", on_click=apply_changes, kwargs=app_args)

if __name__ == "__main__":
    main()
