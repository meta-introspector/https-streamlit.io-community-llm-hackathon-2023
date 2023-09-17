def unassigned_inputs(data):
    
    global app_id
    if selected_app:
        app_id = selected_app
    
    page_size = get_page_size()
    if page_size is '':
        page_size = 10
    else:
        page_size = int(page_size)

    kwargs={}
    st = get_last_id()
    if str:
        kwargs["last_id"]=st

    stream_inputs_response = stub.StreamInputs(
        service_pb2.StreamInputsRequest(
            user_app_id=get_userDataObject(),
            per_page=int(page_size),
            **kwargs
        ),
        metadata=user_metadata
    )
    if stream_inputs_response.status.code != status_code_pb2.SUCCESS:
        yield({"status":stream_inputs_response.status})
        raise Exception("Stream inputs failed, status: " + stream_inputs_response.status.description)
    for input_object in stream_inputs_response.inputs:
        data2 =  requests.get(input_object.data.text.url)
        value =   data2.text
        yield({
            "type": "input",
            #"res": data2.resu
            "id": input_object.id,
            "url": input_object.data.text.url,
            "value":             value})
