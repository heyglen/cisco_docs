
class Command:
    def __init__(self):
        self.name = None
        self.description = None
        self.syntax = list()

    def __str__(self):
        return f'{self.name}'