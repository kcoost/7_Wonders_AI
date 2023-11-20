
class CyclicList:
    def __init__(self, iterable):
        self.iterable = iterable

    def __getitem__(self, i):
        return self.iterable[i % len(self.iterable)]
