import os
from collections.abc import Iterable
import streamlit as st
from clarifai.client.user import User
from clarifai_grpc.grpc.api import resources_pb2

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
            st.write(x)
            yield x
        else:
            if hasattr(x,"apply"):
                yield from x.apply()
            else:
                st.write(x)
                yield x


def act(data):
    if not data:
        return
    for data1 in data:
        
        yield from doapply(data1)  # apply those changes to the api

seen = {}
def myselect(data):
    todo = []
    key = str(data)
    if isinstance(data,str):
        options = st.button(data,
                            key=key + "button"
                            )
    else:

        
        for f in data:
            todo.append(f)

        if key not in seen:
            st.write(data)
            options = st.multiselect(
                "Please select",todo,
                key=key
            )
            seen[key] = options
            st.write("You selected:", options)
            yield options


def decide(data):
    if data:
        if not hasattr(data, '__iter__'):
            #print("The object is iterable.")
            if not isinstance(data, Iterable):
                #print("The object is iterable.")
                #else:
                data = [ "Just" + str(data) ]
                yield myselect(data)  # let the user select which ones
                return
            
            for data1 in data:
                yield from myselect(data1)  # let the user select which ones

def summarize(data):
    for x in data:
        yield x
def sort(data):
    for x in data:
        yield x
def filtering(data):
    for x in data:
        yield x

        
def orient(data):
    yield from summarize(sort(filtering(data)))  # show a summary of the data


def apps():
    # list the apps we have access to
    for app in our_apps:
        yield app

def datasets(app):
    yield "dataset_of_datasets_for" + app.name

def inputs(dataset):
    for x in ("inputa","inputb"):
        yield dataset + x

def observe():
    for app in apps():
        st.write(app)
        for dataset in datasets(app):
            for input in inputs(dataset):
                yield [ app , dataset, input ]

def ooda():
    for sample in observe():
        for oriented in orient(sample):
            for decision in decide(oriented):
                yield from act(decision)

st.set_page_config(layout="wide")

os.environ["CLARIFAI_PAT"] = st.secrets["CLARIFAI_PAT"]
client = User(user_id=st.secrets["clarifai_user_id"])
our_apps = client.list_apps()


#if check_password():
if True: # skip password for now
    for x in ooda():
        if isinstance(x,str):
            st.write(x)
            #yield x
        else:
            if hasattr(x,"apply"):
                for x in  x.apply():
                    st.write(x)
            else:
                st.write(x)


                #action.report()
models = {}
dataset_index = {}
for app in our_apps:
    datasets = app.list_datasets()
    for ds in datasets:
        name = ds.dataset_info.id
        dataset_index[name] = ds
    for model_name in models:
        idn = "cf_dataset_" + model_name.lower()
        if idn not in dataset_index:
            dataset = app.create_dataset(dataset_id=idn)
        else:
            models[model_name].set_dataset(dataset_index[idn])
        models[model_name].sync()


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




