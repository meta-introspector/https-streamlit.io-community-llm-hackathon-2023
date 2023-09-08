import streamlit as st
from clarifai_utils.modules.css import ClarifaiStreamlitCSS
from clarifai.client.user import User
from clarifai_grpc.grpc.api import resources_pb2
from langchain.llms import OpenAI
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler
from langchain.llms import Clarifai
from langchain import PromptTemplate, LLMChain
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, ChatMessageHistory
from langchain.schema import HumanMessage, AIMessage
import streamlit.components.v1 as components


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
        x.apply()


def act(data):
    yield from doapply(data)  # apply those changes to the api


def select(data):

    todo = []
    for f in data:
        todo.append(f)

    options = st.multiselect("Please select", todo)

    st.write("You selected:", options)


def decide(data):
    yield from select(data)  # let the user select which ones


def orient(data):
    yield from summarize(sort(filtering(data)))  # show a summary of the data


def apps():
    # list the apps we have access to 
    pass

# populate
# instructions_data = load_prompt_lists(prompts_dataset())


# from prompts import
#instructions_data = {
#    # key are prompt lists
#}


#def prompts():
#    pass


def datasets(filter):
    pass

def observe():
    yield from inputs(datasets(apps()))  # observe all the data


def ooda():
    act(decide(orient(observe())))  # do it all


st.set_page_config(layout="wide")

os.environ["CLARIFAI_PAT"] = api_key
client = User(user_id=CREATE_APP_USER_ID)
apps = client.list_apps()


if check_password():
    for action in ooda():
        action.report()

dataset_index = {}
for app in apps:
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


# After every input from user, the streamlit page refreshes by default which is unavoidable.
# Due to this, all the previous msgs from the chat disappear and the context is lost from LLM's memory.
# Hence, we need to save the history in seession_state and re-initialize LLM's memory with it.
def show_previous_chats():
    # Display previous chat messages and store them into memory
    chat_list = []
    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                msg = HumanMessage(content=message["content"])
            else:
                msg = AIMessage(content=message["content"])
            chat_list.append(msg)
            st.write(message["content"])
    conversation.memory.chat_memory = ChatMessageHistory(messages=chat_list)


def chatbot():
    if message := st.chat_input(key="input"):
        st.chat_message("user").write(message)
        st.session_state["chat_history"].append({"role": "user", "content": message})
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = conversation.predict(
                    input=message, chat_history=st.session_state["chat_history"]
                )
                # llama response format if different. It seems like human-ai chat examples are appended after the actual response.
                if st.session_state["chosen_llm"].find("lama") > -1:
                    response = response.split("Human:", 1)[0]
                st.text(response)
                message = {"role": "assistant", "content": response}
                st.session_state["chat_history"].append(message)
        st.write("\n***\n")


def oldmain():
    prompt_list = list(instructions_data.keys())
    pat = load_pat()
    models_map, select_map = get_default_models()
    default_llm = "GPT-4"
    llms_map = {"Select an LLM": None}
    llms_map.update(select_map)

    chosen_instruction_key = st.selectbox(
        "Select a prompt",
        options=prompt_list,
        index=(
            prompt_list.index(st.session_state["chosen_instruction_key"])
            if "chosen_instruction_key" in st.session_state
            else 0
        ),
    )

    # Save the chosen option into the session state
    st.session_state["chosen_instruction_key"] = chosen_instruction_key

    if st.session_state["chosen_instruction_key"] != "Select a prompt":
        instruction_title = instructions_data[chosen_instruction_key]["title"]
        instruction = instructions_data[chosen_instruction_key]["instruction"]

        ClarifaiStreamlitCSS.insert_default_css(st)

        with open("./styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

        if "chosen_llm" not in st.session_state.keys():
            chosen_llm = st.selectbox(label="Select an LLM", options=llms_map.keys())
            if chosen_llm and llms_map[chosen_llm] is not None:
                if "chosen_llm" in st.session_state.keys():
                    st.session_state["chosen_llm"] = None
                st.session_state["chosen_llm"] = llms_map[chosen_llm]

    if "chosen_llm" in st.session_state.keys():
        cur_llm = st.session_state["chosen_llm"]
        st.title(f"{instruction_title} {cur_llm}")
        llm = Clarifai(
            pat=pat,
            user_id=models_map[cur_llm]["author"],
            app_id=models_map[cur_llm]["app"],
            model_id=cur_llm,
        )
    else:
        llm = Clarifai(
            pat=pat, user_id="openai", app_id="chat-completion", model_id=default_llm
        )

    # Access instruction by key
    instruction = instructions_data[st.session_state["chosen_instruction_key"]][
        "instruction"
    ]

    template = f"""{instruction} + {{chat_history}}
    Human: {{input}}
    AI Assistant:"""

    prompt = PromptTemplate(
        template=template, input_variables=["chat_history", "input"]
    )

    template = f"""{instruction} + {{chat_history}}
    Human: {{input}}
    AI Assistant:"""

    conversation = ConversationChain(
        prompt=prompt,
        llm=llm,
        verbose=True,
        memory=ConversationBufferMemory(
            ai_prefix="AI Assistant", memory_key="chat_history"
        ),
    )

    # Initialize the bot's first message only after LLM was chosen
    if (
        "chosen_llm" in st.session_state.keys()
        and "chat_history" not in st.session_state.keys()
    ):
        with st.spinner("Chatbot is initializing..."):
            initial_message = conversation.predict(input="", chat_history=[])
            st.session_state["chat_history"] = [
                {"role": "assistant", "content": initial_message}
            ]

    if "chosen_llm" in st.session_state.keys():
        show_previous_chats()
        chatbot()

    st.markdown(
        """
    <style>
    .streamlit-chat.message-container .content p {
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }
    .output {
         white-space: pre-wrap !important;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )
