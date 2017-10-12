
class Command:
    def __init__(self):
        self.name = None
        self.description = None
        self.syntax = list()

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        cls_name = self.__class__.__name__
        return f'<{cls_name} {self.name}>'