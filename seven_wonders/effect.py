from typing import Literal, Optional
from pydantic import BaseModel
from .resources import Production

class VictoryPoints(BaseModel):
    amount: int = 0
    condition: Optional[str] = None
    directions: Optional[list[str]] = None

class Military(BaseModel):
    shields: int = 0

class Science(BaseModel):
    symbol: Literal["sextant", "gear", "script", "any_symbol"] = "any_symbol"

class ReceiveCoins(BaseModel):
    amount: int = 0
    condition: Optional[str] = None
    directions: Optional[list[str]] = None

class ReduceTradeCost(BaseModel):
    resources: list[str] = []
    directions: list[str] = []

class Effect:
    def __init__(self,
                 production: Optional[dict] = None,
                 military: Optional[dict] = None,
                 victory_points: Optional[dict] = None,
                 science: Optional[dict] = None,
                 receive_coins: Optional[dict] = None,
                 reduce_trade_cost: Optional[dict] = None,
                 ):
        self.production = None if production is None else Production(**production)
        self.military = None if military is None else Military(**military)
        self.victory_points = None if victory_points is None else VictoryPoints(**victory_points)
        self.science = None if science is None else Science(**science)
        self.receive_coins = None if receive_coins is None else ReceiveCoins(**receive_coins)
        self.reduce_trade_cost = None if reduce_trade_cost is None else ReduceTradeCost(**reduce_trade_cost)
