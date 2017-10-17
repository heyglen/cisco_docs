

class Syntax:
    def __init__(self):
        self._items = list()
        self.optional = False

    def append(self, item):
        return self._items.append(item)

    def pop(self):
        return self._items.pop()

    def __str__(self):
        return str(self._items).strip('[]')
        # items = list()
        # for item in self._items:
        #     if isinstance(item, Syntax):
        #         items.append(f'[{item}]')
        #     else:
        #         items.append(str(item))
        # return ' '.join(items)