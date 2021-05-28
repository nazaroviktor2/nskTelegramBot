class NotFoundUser(Exception):
    def __init__(self, text):
        self.txt = text


class NotFoundTransfer(Exception):
    def __init__(self, text):
        self.txt = text


class NotFound(Exception):
    def __init__(self, text):
        self.txt = text


class NotFoundLocation(Exception):
    def __init__(self, text):
        self.txt = text


class NotFoundTool(Exception):
    def __init__(self, text):
        self.txt = text


class NotEnoughTools(Exception):
    def __init__(self, text):
        self.txt = text


class HaveNewLocation(Exception):
    def __init__(self, text):
        self.txt = text