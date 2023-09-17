def orient(data):
    toemoji(data)
    yield from summarize(
        sort(
            filtering(data)))  # show a summary of the data
