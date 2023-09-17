################################################################################
# In this section, we set the user authentication, app ID, and the concept we  
# we want to filter by. Change these strings to run your own example.
################################################################################

# USER_ID = 'YOUR_USER_ID_HERE'
# # Your PAT (Personal Access Token) can be found in the portal under Authentification
# PAT = 'YOUR_PAT_HERE'
# APP_ID = 'YOUR_APP_ID_HERE'
# # Change this to filter by your own concept
# CONCEPT_ID = 'people'

##########################################################################
# YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE TO RUN THIS EXAMPLE
##########################################################################

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

