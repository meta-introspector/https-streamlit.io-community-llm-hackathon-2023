import streamlit as st
# objerve /modeoc
from .columns import col1
from .app_args import get_input_id,params,app_args

def get_inputs():
    app_args["input_id"] = st.text_ainput(
        "input Id",
        value=params.get("input_id", ""),
        key="input_id",
        help= "Input Id to load."
    )
    return get_input_id

@limits(calls=5, period=1)
def get_input(input_id):
    get_input_response = stub.GetInput(
        service_pb2.GetInputRequest(
            user_app_id=get_userDataObject(), 
            input_id=input_id
        ),
        metadata=user_metadata
    )
        
    if get_input_response.status.code != status_code_pb2.SUCCESS:
        raise Exception("Get input failed, status: " + get_input_response.status.description)

    input_object = get_input_response.input
    data2 =  requests.get(input_object.data.text.url)
    value =   data2.text

    dt = {
        "type": "input",
        "id": input_object.id,
        "url": input_object.data.text.url,
        "value": value
        }
    yield dt


# @limits(calls=5, period=1)
# def get_input(input_id):
#     get_input_response = stub.GetInput(
#         service_pb2.GetInputRequest(
#             user_app_id=userDataObject, 
#             input_id=input_id
#         ),
#         metadata=metadata
#     )

#     #if get_input_response.status.code == 10000:
#     #    print("RES1",get_input_response)
#     #    print("STAT",get_input_response.status)        
#         #print("RATELIMIT")
#         #return
        
#     if get_input_response.status.code != status_code_pb2.SUCCESS:
#         print("STATUS",get_input_response.status)
#         print("STATUSCODE",stream_inputs_response.status.code)
#         raise Exception("Get input failed, status: " + get_input_response.status.description)

#     input_object = get_input_response.input
#     #print("DEBUG" +str(input_object))
#     #pprint.pprint(
#     return input_object
    
