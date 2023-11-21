from dataclasses import dataclass


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

class Cost(Resources):
    ...

class Yield(Resources):
    total: int = 1
    once: bool = False