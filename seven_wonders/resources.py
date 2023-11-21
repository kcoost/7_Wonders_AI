from dataclasses import dataclass, asdict
from copy import copy

@dataclass
class Resources:
    Coin: int = 0
    Clay: int = 0
    Ore: int = 0
    Stone: int = 0
    Wood: int = 0
    Glass: int = 0
    Loom: int = 0
    Papyrus: int = 0

    def __getitem__(self, item):
        return getattr(self, item)

    def __le__(self, other):
        assert isinstance(other, Resources)
        for resource in asdict(self):
            if self[resource] > other[resource]:
                return False
        return True

    def __add__(self, other):
        copy_self = copy(self)
        for resource, value in asdict(other).items():
            copy_self[resource] += value
        return copy_self


class Cost(Resources):
    ...

class Production(Resources):
    ...