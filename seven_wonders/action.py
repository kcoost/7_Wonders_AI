from dataclasses import dataclass, asdict
import torch

@dataclass
class AvailableCards:
    Academy: bool = False
    Altar: bool = False
    Apothecary: bool = False
    Aqueduct: bool = False
    Archery_Range: bool = False
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

    def as_tensor(self):
        return list(asdict(self).keys()), torch.Tensor(list(asdict(self).values()))

class Plays:
    play_card: bool = False
    discard_card: bool = False
    trade: bool = False

class ActionSpace:
    available_cards = AvailableCards()
    plays = Plays()