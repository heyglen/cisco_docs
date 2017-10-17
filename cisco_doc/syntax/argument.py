

class Argument:

    def __init__(self, argument):
        self.argument = argument

    def __repr__(self):
        # return f"<{self.__class__.__name__} '{self.argument}'>"
        return self.argument

    def __str__(self):
        return self.argument