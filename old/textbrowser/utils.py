from os import remove, listdir


class InvalidQueryException(Exception):
    def __init__(self):
        self.message = 'Invalid user input'


class InvalidRequestError(Exception):
    def __init__(self):
        self.message = 'Failed to request specified resource'

