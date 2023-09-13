import streamlit as st
######################################################################################################
# In this section, we set the user authentication, user and app ID, model details, and the URL of
# the text we want as an input. Change these strings to run your own example.
######################################################################################################
from clarifai_grpc.grpc.api.status import status_code_pb2
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
import simple
import add_text

PAT = st.secrets["CLARIFAI_PAT"]
USER_ID = st.secrets["clarifai_user_id"]

############################################################################
# YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE TO RUN THIS EXAMPLE
############################################################################

def call_workflow(stub, metadata, userDataObject, workflow, data_url):
    st.write("workflow",workflow, "data",data_url)
    post_workflow_results_response = stub.PostWorkflowResults(
        service_pb2.PostWorkflowResultsRequest(
            user_app_id=userDataObject,
            workflow_id=workflow,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(text=resources_pb2.Text(url=data_url))
                )
            ],
        ),
        metadata=metadata,
    )
    if post_workflow_results_response.status.code != status_code_pb2.SUCCESS:
        st.write(post_workflow_results_response.status)
        st.write(post_workflow_results_response)
        raise Exception(
            "Post workflow results failed, status: " + post_workflow_results_response.status.description
        )

    # We'll get one WorkflowResult for each input we used above. Because of one input, we have here one WorkflowResult
    results = post_workflow_results_response.results[0]

    # Each model we have in the workflow will produce one output.
    for output in results.outputs:
        model = output.model

    st.write("Predicted concepts for the model `%s`" % model.id)
    for concept in output.data.concepts:
        st.write("	%s %.2f" % (concept.name, concept.value))

    st.write(results)
    
    # Uncomment this line to st.write the full Response JSON
    fstr = str(results)
    add_text.add_text(stub,userDataObject,metadata,fstr)
