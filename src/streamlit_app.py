import os
import jwt
from ratelimit import limits, RateLimitException
from collections.abc import Iterable
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

os.environ["CLARIFAI_PAT"] = st.secrets["CLARIFAI_PAT"]
password = st.secrets["password"]
client = User(user_id=st.secrets["clarifai_user_id"])
        
col1,col2,col3 = st.columns(3)
col4,col5 = st.columns(2)

oparams = st.experimental_get_query_params()
params = {
    x: oparams[x][0]  for x in oparams
}

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

        
    
@limits(calls=5, period=1)
def get_input(input_id):
    get_input_response = stub.GetInput(
        service_pb2.GetInputRequest(
            user_app_id=get_userDataObject(), 
            input_id=input_id
        ),
        metadata=get_user_metadata( _type="read",
                                    _id=input_id,
                                    _table="inputs",
                                   )

    )

    #if get_input_response.status.code == 10000:
    #    print("RES1",get_input_response)
    #    print("STAT",get_input_response.status)        
        #print("RATELIMIT")
        #return
        
    if get_input_response.status.code != status_code_pb2.SUCCESS:
        #print("STATUS",get_input_response.status)
        #print("STATUSCODE",stream_inputs_response.status.code)
        #raise Exception("Get input failed, status: " + get_input_response.status.description)
        st.error("Cannot find input")
        return 
    input_object = get_input_response.input
    #print("DEBUG" +str(input_object))
    #pprint.pprint(
    data2 =  requests.get(input_object.data.text.url)
    value =   data2.text

    dt = {
        "type": "input",
        "id": input_object.id,
        "url": input_object.data.text.url,
        "value": value
        }
    yield dt


app_args = dict()


with col2:
    # app_args.update(dict(    concept_id = st.text_input(
    #     "Concept",
    #     key="concept_id",
    #     help="Concept id to search for" ,
    #     value =params.get("concept_id","python"))))

    app_args.update(dict(    
        concept_id = list_input(
            "Concept",            
            ["python","Introspector"],
            key="concept_id",            
            default_value="python")))

                         
with col1:
    app_args.update(
        dict(
            app_id = st.text_input("app_id", help="id" , value ="Introspector-LLama2-Hackathon-Demo1"),
            base_url = st.text_input("base_url", key="base-url", value=params.get("base-url",""), help="for the target")
        ))
    
    # number_input(label, min_value=None, max_value=None, value=, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False, label_visibility="visible")
with col1:
    app_args.update(dict(    page_size = st.number_input("Page Size", min_value=1,key="page_size",
                                help="Use a number input widget to allow users to specify the page size. This will control how many items are displayed per page",
                                value=int(params.get("page_size", "3")))))
    #last_id = st.text_input("Last Id", value=params.get("last_id", ""),                            help= "Last Id as a starting token, enter or select the token."                                   ),
with col3:    
    app_args.update(dict(    input_id = st.text_input(
        "input Id",
        value=params.get("input_id", ""),
        key="input_id",
        help= "Input Id to load."
    )))
def show_workflows():
    with col4:
        app_args.update(dict(    
            workflow = list_input(
            "workflow",
            [
                "RakeItUpV3Rewriting_of4",
                "RakeItUpV2rewritesystems",
                "RakeItUpV3Criticaal_Reconstruction_of4",
                "RakeItUpV3review_a_clarifaipython_App_that_will1",
             ],
            default_value="RakeItUpV3Criticaal_Reconstruction_of4",
            
        )))
    
    #num_runs = st.number_input("Number of Runs",                               min_value=1,=int(params.get("num_runs", 1)),                               help="how many times they want to run the selected workflow." ),
    #output_location = st.text_input("Output Location", value=params.get("output_location", ""), help="specify where to store the output, whether it's a file path or a cloud storage location."                                    ),
    #summarize_output = st.checkbox("Summarize Output",                                   value=params.get("summarize_output", False),                                                                      help = "toggle summarization on or off. When summarization is enabled, provide a summary of the outputs; otherwise, display detailed outputs."  ),
    



#####

def get_concept_id():
    return app_args['concept_id']

def get_base_url():
    return app_args['concept_id']

def get_input_id():
    return app_args['input_id']

#def add_workflows(w):
#    global workflows
#    workflows[w.id] = w
    
def get_last_id():
    return app_args['last_id']

def get_app_id():
    return app_args['app_id']

def get_page_size():
    return app_args['page_size']

# Display the result based on parameters


PAT = st.secrets["CLARIFAI_PAT"]
USER_ID =st.secrets["clarifai_user_id"]
channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)
user_metadata = (('authorization', 'Key ' + PAT),)

def check_jwt(kwargs):
    oparams = st.experimental_get_query_params()
    st.write(oparams)
    if "_jwt" in oparams:
        token = oparams["_jwt"][0]
        try:
            decoded_payload = jwt.decode(token, password, algorithms=["HS256"])
            return True
        except jwt.ExpiredSignatureError:
            st.error("JWT token has expired")
            return False
                   #InvalidSignatureError("Signature
        except jwt.InvalidSignatureError as e:
            st.error( f"Invalid _jwtx: {str(e)}")
            #st.write(e)
            return False
            
        except jwt.InvalidTokenError as e:
            st.error( "Invalid JWT token")
            st.write(e)
            return False
        except Exception as e:
            st.error( "ERrror",e)
            st.write(e)
            return False
    else:
        q= st.experimental_get_query_params()
        q.update(app_args)
        encoded_url = urllib.parse.urlencode(q, doseq=True)
        st.error( f"add &_jwt= to query parameter, see https://jtwjwt.streamlit.app/?"+encoded_url)
        return False
            
        #st.write("Decoded JWT Payload:")
        #st.write(decoded_result)


    

def get_user_metadata( _type, #read or write
                       #_id, #what to 
                       #_table="inputs",
                       **kwargs
                      ):

    if _type == "read":
        return user_metadata
    elif _type == "write":
        st.write("get uma test2",kwargs)
        if check_jwt(kwargs):
            st.write("test")
            return user_metadata
        else:
            st.write("error auth")
        
    
userDataObject= None
def get_userDataObject():
    global userDataObject
    if userDataObject is None:
        userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=get_app_id())
    return userDataObject        
    
# globals
seen = {}
our_apps= {}
#app_datasets = {}


def doapply(data):
    for x in data:
        if isinstance(x,str):
            yield x
        else:
            if hasattr(x,"apply"):
                yield from x.apply()
            else:
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

def start_infer_button(workflow,iid, text,url):
    options = st.button(
        workflow,
        on_click=run_infer,
        kwargs={
            #"concept":selected_concept,
            "value":text,
            "url":url
        },
        key= text + "button",
        help=str(text)
    )

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
            yield from myselect([data1 for data1 in data.items()])  # let the user select which ones
    show_workflows()

    start_infer_button(get_workflow(),
                       iid = get_input_id(),
                       text="text",
                       url="url")

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

def get_workflow():
    if "workflow" in st.session_state:
        return st.session_state["workflow"]
    else:
        for x in  st.session_state:
            v = st.session_state[x]
            st.write("DEBUG1",x,v)
        return "default-workflow"
    

def run_infer(value, url):

    #st.write("infer",value, url)

    #st.write("selected",wf)
    workflow = get_workflow()
    st.write("workflow",workflow)
    data_url = url

    ci = get_concept_id()

    concepts=[workflow]
    if ci :
        concepts.append(ci)
    try:

        ret = call_api.call_workflow(stub,
                                     get_user_metadata( _type="write",
                                                        _call="workflow",
                                                        _on=data_url,
                                                        _for=concepts)
                                     , get_userDataObject(), workflow, data_url, concepts)
            
        #st.write(ret)
    except Exception as e:
        st.write("ERROR",e)
        raise e

def workflow_button(workflow):
    
    options = st.button(workflow,
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
            
def to_url(data):
    if isinstance(data, types.GeneratorType):
        return "GEN"
    elif "value" in data:
        va = data["value"]
        if "url" in data:
            url = data["url"]
            aid = data["id"]
            name = va + "button"
            
            #st.write("translate this into a structured emoji representation?",url)

            # Get the current URL as a string
            q= st.experimental_get_query_params()
            q.update(app_args)
            encoded_url = urllib.parse.urlencode({"url":url}, doseq=True)
            q["data_url"] = encoded_url
            q["input_id"] = aid
            #workflow = get_workflow()


            # generic
            #for x in st.session_state:
            #    q[f"st_{x}"] = str(st.session_state[x])                
                #q[f"st_{x}"] = str(st.session_state[x])
                
            #q["input_name"] = name
            #q["input_value"] = va # skip this for shortness


            encoded_query = urllib.parse.urlencode(q, doseq=True)
            #st.write(encoded_query)            
            
            #st.markdown(f"* [#{aid}](/?{encoded_query})")
            #data = {}
            data["link_text"] = f"* [#{aid}](/{get_base_url()}?{encoded_query})"
            return data
            #st.write(parsed_url)
            # Replace the query part of the URL with the new string
            #new_url = parsed_url._replace(query=encoded_query).geturl()
            # Write the new URL as a link
            #st.write(f"[New URL]", new_url)
        else:
            return "OTHER"

    return "NONE"


def summarize(data):

    # lets see if we can use emojis to summarize.
    #toemoji(data)
    #st.write("DEBUG",data)
    #if isinstance(data, generato):
    
    akeys = {}

    if isinstance(data, Iterable):
        if isinstance(data, types.GeneratorType):
            for x in data:
                yield x
                #u = to_url(x)
                #st.write("DEBUG1",x)
                #total.append(x)
        else:
            #st.write("Sum Object is iterable", type(data).__name__, data, )
            for x in data:
                u = to_url(x)
                #st.write("DEBUG2",x)
                v = x["value"]

                akeys[v] = x
    else:
        st.write("Sum Object not an iterable")
        yield data
        
    #st.write("total")
    #st.write(total)
    #st.dataframe(total)
    #for v in total:

    yield akeys
    st.selectbox("Input",list(akeys.keys()))
    #(total, num_rows="dynamic",
    #               height=100,
    #               use_container_width=True,
    #               column_order=["value",])


def sort(data):
    
    if isinstance(data, Iterable):
        if isinstance(data, types.GeneratorType):
            
            ret= sorted([x for x in data])
            st.write(ret)
            yield ret

        else:
            #st.write("Sort Object is iterable",type(data).__name__,data)
            #for x in data:
            #y = ata
            yield data

    else:
        st.write("Sort Object not an iterable",data)
        yield data


def filtering(data):
    
    if isinstance(data,str):
        yield data
        st.write("filter",data)
        return
    if isinstance(data, Iterable):
        if isinstance(data, types.GeneratorType):
            for x in data:
                st.write("filter",x)
                yield x
        else:            
            if "value" in data:
                #v = data["value"]
                #st.write("VALUE",data)
                yield data
            else:
                st.write("Filtering Object is iterable",type(data).__name__,data)
    else:
        st.write("Filtering Object not an iterable", data)
        yield data
        
def orient(data):
    #toemoji(data)
    for x in  filtering(data) :
        #st.write("orient",x)
        yield x
all_apps = []
selected_app = None


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
#app_id = None

def find_inputs(concept_id):
    max_count = get_page_size()
    user_app_id=get_userDataObject()
    #st.write("search for concepts",concept_id)
    #st.write("user data",user_app_id)
    #st.write("stub",stub)
    #st.write("user metadata",user_metadata)
    post_annotations_searches_response = stub.PostAnnotationsSearches(
        service_pb2.PostAnnotationsSearchesRequest(
            user_app_id=user_app_id,
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
        metadata=get_user_metadata( _type="read",
                                    _concept_id=concept_id,
                                    _table="concepts",
                                   )
                                    
    )
    
    if post_annotations_searches_response.status.code != status_code_pb2.SUCCESS:
        st.write("Post searches failed, status: " + post_annotations_searches_response.status.description)
        

    count = 0 
    for hit in post_annotations_searches_response.hits:
        value  = str(hit)
        for x in hit.ListFields():
            for y in x:
                if isinstance(y, resources_pb2.Input):
                    input_object = y 
                    data2 =  requests.get(input_object.data.text.url)
                    value =   data2.text
                    count = count +1
                    if count < max_count:
                        dt = {
                                "type": "input",
                                "id": input_object.id,
                                "url": input_object.data.text.url,
                                "value": value
                            }
                        #st.write(dt)
                        yield(dt)
                    else:
                        return #leave


def observe():
    #for x in prepare():
    #    yield x
    iid = get_input_id()

    if iid:
        yield from get_input(iid)
        return
    else:
        yield from find_inputs(get_concept_id())


def ooda():
    samples = []
    for sample in observe():
        for oriented in orient(sample):
            #st.write("orient",oriented)
            samples.append(oriented)
    #st.write("SAMPLE",samples)
    for suma in summarize( samples):
        for decision in decide(suma):
            yield from act(decision)


# taken from https://gist.githubusercontent.com/iankelk/7e46c9935442ba01853b1689ff4a5038/raw/a261f99e6dd9cef6cc3d9ee04648df40232072d9/C-everything.py
def load_pat():
    if "CLARIFAI_PAT" not in st.secrets:
        st.error("You need to set the CLARIFAI_PAT in the secrets.")
        st.stop()
    return st.secrets.CLARIFAI_PAT


def main():
    global our_apps
    our_apps = client.list_apps()
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

args = {}


def get_args():
    params = st.experimental_get_query_params()
    


# Function to apply changes
def apply_changes(**args):
    # Update URL with current parameter values
    st.experimental_set_query_params(**args  )


if __name__ == "__main__":
    main()
