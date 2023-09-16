import os
import os, types
from ratelimit import limits, RateLimitException
from collections.abc import Iterable
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
import streamlit as st
import types
import call_api
import emojis
import asyncio
import requests
import urllib.parse        
from clarifai.client.user import User
from clarifai_grpc.grpc.api import resources_pb2
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
import streamlit.runtime.scriptrunner.script_runner
import streamlit.web.server.server
import streamlit.web.server.routes

import tornado.httpserver
import tornado.ioloop
import tornado.iostream
import tornado.routing
import tornado.tcpserver
import tornado.web
import tornado.websocket
import traceback
import inspect
st.write(inspect.getsourcefile(streamlit.web.server.server))

target = "backups"
if not os.path.exists(target):
    os.mkdir(target)
    #copy abackup of server
with open(os.path.join(target,"server.py"),"w") as fo:
    with open(inspect.getsourcefile(streamlit.web.server.server),"r") as fi:
        fo.write(fi.read())

ctx =streamlit.runtime.scriptrunner.script_runner.get_script_run_ctx()

# st.write("CTX",ctx)
# st.write("CTX",str(ctx))
# st.write("Sess",dir(ctx))
# for x in dir(ctx):
#     st.write("DEBUG",x,getattr(ctx,x,"None"))


    
# ctxScriptRunContextScriptRunContext(session_id='6ab6368d-3bf6-492e-a2d0-d8d3a5733e71', _enqueue=<bound method ScriptRunner._enqueue_forward_msg of ScriptRunner(_session_id='6ab6368d-3bf6-492e-a2d0-d8d3a5733e71', _main_script_path='./src/streamlit_app.py', _uploaded_file_mgr=MemoryUploadedFileManager(endpoint='/_stcore...
# A context object that contains data for a "script run" - that is,
# data that's scoped to a single ScriptRunner execution (and therefore also
# scoped to a single connected "session").

# ScriptRunContext is used internally by virtually every `st.foo()` function.
# It is accessed only from the script thread that's created by ScriptRunner.

# Streamlit code typically retrieves the active ScriptRunContext via the
# `get_script_run_ctx` function.
# command_tracking_deactivatedbool	True
# cursorsdict	{}
# dg_stacklist	[]
# form_ids_this_runset	set()
# gather_usage_statsbool	True
# page_script_hashstr	'04d9c6d3425fdb18dfa2143151c97767'
# query_stringstr	''
# session_idstr	'6ab6368d-3bf6-492e-a2d0-d8d3a5733e71'
# session_stateSafeSessionState	Thread-safe wrapper around SessionState.
# tracked_commandslist	[name: "write" args { k: "1" t: "streamlit.runtime.scriptrunner.script_run_context.ScriptRunContext" p: 1 } ]
# tracked_commands_counterCounter	Counter({'write': 1})
# uploaded_file_mgrMemoryUploadedFileManager	MemoryUploadedFileManager(endpoint='/_stcore/upload_file')
# user_infodict	{'email': 'test@localhost.com'}
# widget_ids_this_runset	set()
# widget_user_keys_this_runset	set()
# enqueuemethod	Enqueue a ForwardMsg for this context's session.
# on_script_startmethod	No docs available
# resetmethod	No docs available
# ScriptRunContext(session_id='6ab6368d-3bf6-492e-a2d0-d8d3a5733e71', _enqueue=<bound method ScriptRunner._enqueue_forward_msg of ScriptRunner(_session_id='6ab6368d-3bf6-492e-a2d0-d8d3a5733e71', _main_script_path='./src/streamlit_app.py', _uploaded_file_mgr=MemoryUploadedFileManager(endpoint='/_stcore/upload_file'), _script_cache=<streamlit.runtime.scriptrunner.script_cache.ScriptCache object at 0x7f305f154d90>, _user_info={'email': 'test@localhost.com'}, _client_state=, _session_state=<streamlit.runtime.state.safe_session_state.SafeSessionState object at 0x7f305cc78670>, _requests=<streamlit.runtime.scriptrunner.script_requests.ScriptRequests object at 0x7f304dc0b2e0>, on_event=<blinker.base.Signal object at 0x7f304dc0ba30>, _execing=True, _script_thread=<Thread(ScriptRunner.scriptThread, started 139845467305536)>)>, query_string='', session_state=<streamlit.runtime.state.safe_session_state.SafeSessionState object at 0x7f305cc78670>, uploaded_file_mgr=MemoryUploadedFileManager(endpoint='/_stcore/upload_file'), page_script_hash='04d9c6d3425fdb18dfa2143151c97767', user_info={'email': 'test@localhost.com'}, gather_usage_stats=True, command_tracking_deactivated=False, tracked_commands=[name: "write" args { k: "1" t: "streamlit.runtime.scriptrunner.script_run_context.ScriptRunContext" p: 1 } time: 5345 ], tracked_commands_counter=Counter({'write': 1}), _set_page_config_allowed=False, _has_script_started=True, widget_ids_this_run=set(), widget_user_keys_this_run=set(), form_ids_this_run=set(), cursors={0: RunningCursor(_parent_path=(), _index=1)}, dg_stack=[])
                                                                                                                                                                                                                                                                                                             
#st.write("Sess STate",ctx.session_state._state)
#st.write("Sess STate",dir(ctx.session_state._state))
#st.write("Sess",dir(ctx.session_state))


values = {}


#st.write("current",tornado.ioloop.IOLoop.current())

#import pdb
#pdb.set_trace()

# for x in inspect.stack():
#     st.write("CALLBACK",str(x))
#     #st.write(dir(x))
#     st.write("CALLBACK1",x.frame)
#     st.write("CALLBACK2",x.frame.f_globals)
#     st.write("CALLBACK3",x.code_context)
            
#for line in traceback.format_stack():
#    st.write(line.strip())
#    st.write(line)
        
_io_loops= {}
_io_loop = tornado.ioloop.IOLoop.current()
#st.write("current",type(_io_loop).__name__)
if _io_loop not in _io_loops:
    _io_loops[_io_loop] = True
    #st.write("started ")

    asyncio_loop = _io_loop.asyncio_loop  # type: ignore

    #st.write("asyncio_loop ",asyncio_loop)
    tasks = asyncio.all_tasks(asyncio_loop)  # type: ignore

    asyncio_loop.set_debug(True)
    #for x in dir(asyncio_loop):
    #    st.write(x)
    #st.write("asyncio_loop tasks", tasks)
#if hasattr(asyncio, "all_tasks"):  # py37

#        else:
#           tasks = asyncio.Task.all_tasks(asyncio_loop)


    #modify_times = {}  # type: Dict[str, float]
    #callback = functools.partial(_reload_on_update, modify_times)
    #scheduler = ioloop.PeriodicCallback(callback, check_time)
    #scheduler.start()


# for x in list(globals()):
#     v = globals()[x]

#     if isinstance(v, types.ModuleType):
#         values[x] = globals()[x]
    

st.write("server")
#st.dataframe(dir(streamlit.web.server.server))
for module in values:
    st.write(module)
    #st.write(help(module))
    #for x in values[module]:
    #    v = values[module][x]
    #    st.write(module,x,v)
    #st.dataframe(dir(module))

#st.dataframe(dir(streamlit))


raise Exception("test")

oparams = st.experimental_get_query_params()
params = {
    x: oparams[x][0]  for x in oparams
}
        
# modes
class ConceptInputs():
    pass
class AllInputs():
    pass

class OneInputs():
    pass
    
@limits(calls=5, period=1)
def get_input(input_id):
    get_input_response = stub.GetInput(
        service_pb2.GetInputRequest(
            user_app_id=get_userDataObject(), 
            input_id=input_id
        ),
        metadata=user_metadata
    )

    #if get_input_response.status.code == 10000:
    #    print("RES1",get_input_response)
    #    print("STAT",get_input_response.status)        
        #print("RATELIMIT")
        #return
        
    if get_input_response.status.code != status_code_pb2.SUCCESS:
        #print("STATUS",get_input_response.status)
        #print("STATUSCODE",stream_inputs_response.status.code)
        raise Exception("Get input failed, status: " + get_input_response.status.description)

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

modes = {
    "concept-inputs" : ConceptInputs(),
    "all-inputs": AllInputs(),
    "one-input": OneInputs(),
}        

app_args = dict(
    mode = st.text_input("Mode", help="Mode to use", key="mode",value=params.get("mode","concept-inputs")),
    #st.selectbox("mode",
    #modes,
    #key="mode",
    #                             #on_change=mode_selected,                                 
    #                             help="choose which mode to use."),
    concept_id = st.text_input(
        "ConceptID",
        key="concept_id",
        help="Concept id to search for" ,
        value =params.get("concept_id","python")),
    
    app_id = st.text_input("app_id", help="id" , value ="Introspector-LLama2-Hackathon-Demo1"),
    # number_input(label, min_value=None, max_value=None, value=, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False, label_visibility="visible")
    page_size = st.number_input("Page Size", min_value=1,key="page_size",
                                help="Use a number input widget to allow users to specify the page size. This will control how many items are displayed per page",
                                value=int(params.get("page_size", "3"))),
    #last_id = st.text_input("Last Id", value=params.get("last_id", ""),                            help= "Last Id as a starting token, enter or select the token."                                   ),
    input_id = st.text_input(
        "input Id",
        value=params.get("input_id", ""),
        key="input_id",
        help= "Input Id to load."
    ),
    
    workflow = st.text_input(
        "Workflow",
        value=params.get(
            "workflow",
            "RakeItUpV3Critical_Reconstruction_of4"),
        key="workflow"
    )
    #num_runs = st.number_input("Number of Runs",                               min_value=1,=int(params.get("num_runs", 1)),                               help="how many times they want to run the selected workflow." ),
    #output_location = st.text_input("Output Location", value=params.get("output_location", ""), help="specify where to store the output, whether it's a file path or a cloud storage location."                                    ),
    #summarize_output = st.checkbox("Summarize Output",                                   value=params.get("summarize_output", False),                                                                      help = "toggle summarization on or off. When summarization is enabled, provide a summary of the outputs; otherwise, display detailed outputs."  ),
    )


#####
for x in oparams:
    if x in st.session_state:
        # fixme validate thise
        if x in ("mode","input_id","workflow"):
            st.write("DEBUG",x,st.session_state[x],oparams[x][0])
            #st.session_state[x] = oparams[x][0]


#####

def get_concept_id():
    return app_args['concept_id']

def get_input_id():
    return app_args['input_id']

#def add_workflows(w):
#    global workflows
#    workflows[w.id] = w
    
def get_last_id():
    return app_args['last_id']

def get_mode():
    return app_args['mode']

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

def get_workflow():
    if "workflow" in st.session_state:
        return st.session_state["workflow"]
    else:
        for x in  st.session_state:
            v = st.session_state[x]
            st.write("DEBUG",x,v)
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
        ret = call_api.call_workflow(stub, user_metadata, get_userDataObject(), workflow, data_url, concepts)
        #st.write(ret)
    except Exception as e:
        st.write("ERROR",e)
        raise e


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
            q["mode"] = "one-input"
            encoded_url = urllib.parse.urlencode({"url":url}, doseq=True)
            q["data_url"] = encoded_url
            q["input_id"] = aid
            #q["1workflow"] = get_workflow()


            # generic
            #for x in st.session_state:
            #    q[f"st_{x}"] = str(st.session_state[x])                
                #q[f"st_{x}"] = str(st.session_state[x])
                
            #q["input_name"] = name
            #q["input_value"] = va # skip this for shortness


            encoded_query = urllib.parse.urlencode(q, doseq=True)
            #st.write(encoded_query)            
            
            st.markdown(f"* share [input_link {encoded_query}](/?{encoded_query})")


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
    st.write("search for concepts",concept_id)
    st.write("user data",user_app_id)
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
        metadata=user_metadata
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
                        st.write(dt)
                        yield(dt)
                    else:
                        return #leave


def observe():
    #for x in prepare():
    #    yield x
    amode =get_mode()
    st.write(amode)
    
    if amode == "concept-inputs":
        yield from find_inputs(get_concept_id())
    elif amode == "one-input":
        #http://192.168.1.163:8502/?concept_id=python&app_id=Introspector-LLama2-Hackathon-Demo1&page_size=3&workflow=RakeItUpV3Critical_Reconstruction_of4&data_url=https%3A%2F%2Fdata.clarifai.com%2Forig%2Fusers%2Frxngfnlo5uhx%2Fapps%2FIntrospector-LLama2-Hackathon-Demo1%2Finputs%2Ftext%2Fe0062df82800d031e8a8bfc3a6b21213&
        # input_id=f78ca91871b74e249033d5179e730dd9&mode=one-input
        yield from get_input(get_input_id())
    else:
        st.write("something")

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


# def get_default_models():
#     if "DEFAULT_MODELS" not in st.secrets:
#         st.error("You need to set the default models in the secrets.")
#         st.stop()
#     models_list = [x.strip() for x in st.secrets.DEFAULT_MODELS.split(",")]
#     models_map = {}
#     select_map = {}
#     for i in range(len(models_list)):
#         m = models_list[i]
#         id, rem = m.split(":")
#         author, app = rem.split(";")
#         models_map[id] = {}
#         models_map[id]["author"] = author
#         models_map[id]["app"] = app
#         select_map[id + " : " + author] = id
#     return models_map, select_map

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

    # for app in our_apps:
    #     datasets = app.list_datasets()
    #     for ds in datasets:
    #         name = ds.dataset_info.id
    #         if app not in app_datasets:
    #             app_datasets[app.name]={}
    #         if name not in app_datasets[app.name]:
    #             app_datasets[app.name][name] = ds
        
    #         dataset_index[name] = ds
    # for model_name in models:
    #     idn = "cf_dataset_" + model_name.lower()
    #     if idn not in dataset_index:
    #         dataset = app.create_dataset(dataset_id=idn)
    #     else:
    #         models[model_name].set_dataset(dataset_index[idn])
    #     models[model_name].sync()

args = {}


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



if __name__ == "__main__":
    main()
