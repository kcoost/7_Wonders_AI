import random
from dataclasses import dataclass, asdict
from copy import copy

random.seed(0)

@dataclass
class Production:
    clay: int = 0
    ore: int = 0
    stone: int = 0
    wood: int = 0
    wood_clay: int = 0
    stone_clay: int = 0
    clay_ore: int = 0
    stone_wood: int = 0
    wood_ore: int = 0
    ore_stone: int = 0
    any_raw_material: int = 0
    glass: int = 0
    loom: int = 0
    papyrus: int = 0
    any_good: int = 0

    def __add__(self, other):
        copy_self = copy(self)
        for resource, value in asdict(other).items():
            copy_self[resource] += value
        return copy_self

@dataclass
class SellableProduction:
    clay: int = 0
    ore: int = 0
    stone: int = 0
    wood: int = 0
    wood_clay: int = 0
    stone_clay: int = 0
    clay_ore: int = 0
    stone_wood: int = 0
    wood_ore: int = 0
    ore_stone: int = 0
    glass: int = 0
    loom: int = 0
    papyrus: int = 0

    def max_amount(self, resource: str):
        amount = 0
        for sellable_resource, value in asdict(self).items():
            if sellable_resource in resource:
                amount += value
        return amount

    def remove(self, resource: str, amount: int):
        # try to remove from pure productions
        if self[resource] >= amount:
            self[resource] -= amount
            return

        # remove resources from random mixed productions
        while amount > 0:
            productions = [p for p, n in asdict(self).items() if resource in p and n > 0]
            production = random.choice(productions)
            self[production] -= 1
            amount -= 1

@dataclass
class Cost:
    coins: int = 0 # TODO
    clay: int = 0
    ore: int = 0
    stone: int = 0
    wood: int = 0
    glass: int = 0
    loom: int = 0
    papyrus: int = 0

    # def __getitem__(self, item):
    #     return getattr(self, item)

    # def __le__(self, other):
    #     assert isinstance(other, Cost)
    #     for resource in asdict(self):
    #         if self[resource] > other[resource]:
    #             return False
    #     return True

    # def __add__(self, other):
    #     copy_self = copy(self)
    #     for resource, value in asdict(other).items():
    #         copy_self[resource] += value
    #     return copy_self

@dataclass
class Resources:
    clay: int = 0
    ore: int = 0
    stone: int = 0
    wood: int = 0
    glass: int = 0
    loom: int = 0
    papyrus: int = 0


@dataclass
class TradeCost:
    clay: int = 2
    ore: int = 2
    stone: int = 2
    wood: int = 2
    glass: int = 2
    loom: int = 2
    papyrus: int = 2