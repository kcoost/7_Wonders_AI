from dataclasses import asdict, dataclass

from .resources import TradeCost, Production, SellableProduction
from .cards import CardList
import torch



@dataclass
class CityState:
    production: Production = Production()
    card_list: CardList = CardList()
    coins: int = 3
    shields: int = 0
    n_wonder: int = 0

    n_brown: int = 0
    n_grey: int = 0
    n_red: int = 0
    n_blue: int = 0
    n_green: int = 0
    n_yellow: int = 0
    n_purple: int = 0

    # TODO make class?
    sextants: int = 0
    gears: int = 0
    scripts: int = 0
    any_symbols: int = 0

    n_military_defeat: int = 0
    military_result_I: int = 0
    military_result_II: int = 0
    military_result_III: int = 0
    base_victory_points: int = 0

    west_trade_costs: TradeCost = TradeCost()
    east_trade_costs: TradeCost = TradeCost()

    sellable_production: SellableProduction = SellableProduction()

    def to_tensor(self):
        values = []
        for field in asdict(self).values():
            if isinstance(field, dict):
                values += list(field.values())
            elif isinstance(field, int):
                values.append(field)
            else:
                raise ValueError
        return torch.Tensor(values)
