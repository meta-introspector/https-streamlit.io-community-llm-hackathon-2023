from app_args
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