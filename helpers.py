def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def batch_from_iter(iterator, size):
    buffer = []
    for number, element in enumerate(iterator, start=1):
        buffer.insert(0, element)
        if number % size == 0:
            yield buffer
            buffer.clear()
    if len(buffer) > 0:
        yield buffer
