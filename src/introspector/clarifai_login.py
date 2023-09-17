PAT = st.secrets["CLARIFAI_PAT"]
USER_ID =st.secrets["clarifai_user_id"]
channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)
user_metadata = (('authorization', 'Key ' + PAT),)
os.environ["CLARIFAI_PAT"] = st.secrets["CLARIFAI_PAT"]
client = User(user_id=st.secrets["clarifai_user_id"])
userDataObject= None

# taken from https://gist.githubusercontent.com/iankelk/7e46c9935442ba01853b1689ff4a5038/raw/a261f99e6dd9cef6cc3d9ee04648df40232072d9/C-everything.py
def load_pat():
    if "CLARIFAI_PAT" not in st.secrets:
        st.error("You need to set the CLARIFAI_PAT in the secrets.")
        st.stop()
    return st.secrets.CLARIFAI_PAT

def get_userDataObject():
    global userDataObject
    if userDataObject is None:
        userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=get_app_id())
    return userDataObject        
