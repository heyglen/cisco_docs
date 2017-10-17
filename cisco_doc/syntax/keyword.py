

class Keyword:

    def __init__(self, keyword):
        self.keyword = keyword

    def __repr__(self):
        # return f"<{self.__class__.__name__} '{self.keyword}'>"
        return self.keyword

    def __str__(self):
        return self.keyword