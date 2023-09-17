
def act(data):
    if not data:
        return
    for data1 in data:
        yield from doapply(data1)  # apply those changes to the api
