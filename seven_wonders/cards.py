import torch
from dataclasses import dataclass, asdict
from .resources import Cost
from .effect import Effect

COLOUR_MAP = {"brown": "\033[33m",
              "grey": "\033[37m",
              "blue": "\033[34m",
              "red": "\033[31m",
              "green": "\033[92m",
              "yellow": "\033[1;33m",
              "purple": "\033[35m"}

@dataclass
class CardList:
    Academy: bool = False
    Altar: bool = False
    Apothecary: bool = False
    Aqueduct: bool = False
    Archery_range: bool = False
    Arena: bool = False
    Arsenal: bool = False
    Barracks: bool = False
    Baths: bool = False
    Bazar: bool = False
    Brickyard: bool = False
    Builders_guild: bool = False
    Caravansery: bool = False
    Chamber_of_commerce: bool = False
    Circus: bool = False
    Clay_pit: bool = False
    Clay_pool: bool = False
    Courthouse: bool = False
    Craftsmens_guild: bool = False
    Dispensary: bool = False
    East_trading_post: bool = False
    Excavation: bool = False
    Forest_cave: bool = False
    Fortifications: bool = False
    Forum: bool = False
    Foundry: bool = False
    Gardens: bool = False
    Glassworks: bool = False
    Guard_tower: bool = False
    Haven: bool = False
    Laboratory: bool = False
    Library: bool = False
    Lighthouse: bool = False
    Lodge: bool = False
    Loom: bool = False
    Lumber_yard: bool = False
    Magistrates_guild: bool = False
    Marketplace: bool = False
    Mine: bool = False
    Observatory: bool = False
    Ore_vein: bool = False
    Palace: bool = False
    Pantheon: bool = False
    Pawnshop: bool = False
    Philosophers_guild: bool = False
    Press: bool = False
    Quarry: bool = False
    Sawmill: bool = False
    School: bool = False
    Scientists_guild: bool = False
    Scriptorium: bool = False
    Senate: bool = False
    Shipowners_guild: bool = False
    Siege_workshop: bool = False
    Spies_guild: bool = False
    Stables: bool = False
    Statue: bool = False
    Stockade: bool = False
    Stone_pit: bool = False
    Strategists_guild: bool = False
    Study: bool = False
    Tavern: bool = False
    Temple: bool = False
    Theater: bool = False
    Timber_yard: bool = False
    Town_hall: bool = False
    Traders_guild: bool = False
    Training_ground: bool = False
    Tree_farm: bool = False
    University: bool = False
    Vineyard: bool = False
    Walls: bool = False
    West_trading_post: bool = False
    Workers_guild: bool = False
    Workshop: bool = False

    def __getitem__(self, idx: int):
        return list(asdict(self).keys())[idx]

    def to_tensor(self):
        return torch.Tensor(list(asdict(self).values()))

class Card:
    def __init__(
        self,
        age: str,
        n_players: int,
        name: str,
        colour: str,
        chains: list[str],
        cost: dict[str, int],
        effect: dict[str, dict]
    ):
        self.age = age
        self.name = name
        self.n_players = n_players
        self.colour = colour
        self.base_cost = Cost(**cost)
        self.chains = chains
        self.effect = Effect(**effect)

    def __repr__(self):
        return COLOUR_MAP[self.colour] + self.name

    def is_chained(self, card_list: CardList):
        for card_name in asdict(card_list).keys():
            if card_name in self.chains:
                return True
        return False
