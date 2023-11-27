from enum import Enum
from dataclasses import dataclass, asdict
from .cards import Card

class Action(Enum):
    play_card: str = "play card"
    stage_wonder: str = "stage wonder"
    discard: str = "discard"

@dataclass
class Trade:
    coins: int = 0
    clay: int = 0
    ore: int = 0
    stone: int = 0
    wood: int = 0
    glass: int = 0
    loom: int = 0
    papyrus: int = 0

    def __repr__(self):
        if self.coins == 0:
            return "None"

        texts = []
        for resource, amount in asdict(self).items():
            if resource == "coins":
                continue
            if amount == 0:
                continue
            texts.append(f"{amount} {resource}s") # .capitalize()

        return ", ".join(texts) + f", costing {self.coins} coins"

# class Trade:
#     west: SingleTrade = SingleTrade()
#     east: SingleTrade = SingleTrade()

#     def __repr__(self):
#         return f"West trades: {self.west}\nEast trades: {self.east}"

@dataclass
class Play:
    card: Card
    spent_coins: int
    trade_west: Trade
    trade_east: Trade
    action: Action