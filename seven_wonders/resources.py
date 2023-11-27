import torch
import random
from itertools import product
from dataclasses import dataclass, asdict
from copy import copy

#random.seed(0)

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
        copy_self = asdict(copy(self))
        for resource, value in asdict(other).items():
            copy_self[resource] += value
        return Production(**copy_self)

    def goods_combinations(self):
        combinations = []
        base_resources = self.glass*["glass"] + self.loom*["loom"] + self.papyrus*["papyrus"]
        if self.any_good == 0:
            return [base_resources]
        for products in product(*self.any_good*[["glass", "loom", "papyrus"]]):
            combinations.append(base_resources + list(products))
        return combinations

    def raw_materials_combinations(self):
        iters = [self.wood_clay*["wood", "clay"],
                self.stone_clay*["stone", "clay"],
                self.clay_ore*["clay", "ore"],
                self.stone_wood*["stone", "wood"],
                self.wood_ore*["wood", "ore"],
                self.ore_stone*["ore", "stone"],
                self.any_raw_material*["clay", "ore", "stone", "wood"]]

        combinations = []
        base_resources = self.clay*["clay"] + self.ore*["ore"] + self.stone*["stone"] + self.wood*["wood"]
        if len(iters) == 0:
            return [base_resources]
        for products in product(*iters):
            combinations.append(base_resources + list(products))
        return combinations

    def can_afford(self, cost: Cost):
        # check coins separately

        # check goods
        combinations = self.goods_combinations()
        afford_good = False
        for combination in combinations:
            if cost.glass <= combination.count("glass") and cost.loom <= combination.count("loom") and cost.papyrus <= combination.count("papyrus"):
                afford_good = True

        # check raw materials
        afford_raw_material = False
        for combination in combinations:
            if cost.clay <= combination.count("clay") and cost.ore <= combination.count("ore") and cost.stone <= combination.count("stone") and cost.wood <= combination.count("wood"):
                afford_raw_material = True
        return afford_good and afford_raw_material


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
        if getattr(self, resource) >= amount:
            setattr(self, resource, getattr(self, resource) - amount)
            return

        # remove resources from random mixed productions
        while amount > 0:
            productions = [p for p, n in asdict(self).items() if resource in p and n > 0]
            production = random.choice(productions)
            setattr(self, production, getattr(self, production) - 1)
            amount -= 1

@dataclass
class Resources:
    clay: int = 0
    ore: int = 0
    stone: int = 0
    wood: int = 0
    glass: int = 0
    loom: int = 0
    papyrus: int = 0

    def add(self, resource: str, amount: int):
        old_value = getattr(self, resource)
        setattr(self, resource, old_value + amount)

    def __add__(self, other: "Resources"):
        copy_self = asdict(copy(self))
        for resource, value in asdict(other).items():
            copy_self[resource] += value
        return Resources(**copy_self)


@dataclass
class TradeCost:
    clay: int = 2
    ore: int = 2
    stone: int = 2
    wood: int = 2
    glass: int = 2
    loom: int = 2
    papyrus: int = 2