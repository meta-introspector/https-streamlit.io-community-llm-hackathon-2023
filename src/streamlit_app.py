import os
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


# all_apps = []
# app_args ={}
# args = {}
# dataset_index = {}
# models = {}
#our_apps= {}
# seen = {}
# selected_app = None

#########
from introspector.ooda import ooda
def main():

    for x in ooda():
        #this is a stream of data you can process
            if isinstance(x,str):
                st.write("DEBUG STR",x)
                pass
            else:
                if hasattr(x,"apply"):
                    for x in  x.apply():
                        st.write("app",x)
                    else:
                        st.write("other",x)
                        pass                        



if __name__ == "__main__":
    main()
