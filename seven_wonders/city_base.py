from copy import deepcopy
import random
import torch
from torch.nn.functional import softmax
from dataclasses import asdict, dataclass
from .players import Player
from .city_state import CityState, CardList
from .plays import Play
from .action import Action
from .effect import Effect
from .resources import Production, TradeCost, Cost, Resources, SellableProduction
from .cards import Card

random.seed(0)
torch.manual_seed(0)


@dataclass
class City:
    production: Production
    sellable_production: SellableProduction
    wonder_costs: tuple[Cost]
    wonder_effects: tuple[Effect]

    def __init__(self, name: str, player: Player):
        self.name = name
        self.player = player

        self.card_list = CardList()
        self.coins = 3
        self.shields = 0
        self.n_wonder = 0

        self.n_brown = 0
        self.n_grey = 0
        self.n_red = 0
        self.n_blue = 0
        self.n_green = 0
        self.n_yellow = 0
        self.n_purple = 0

        # TODO make class?
        self.sextants = 0
        self.gears = 0
        self.script = 0
        self.any_symbol = 0

        self.n_military_defeat = 0
        self.military_result_I = 0
        self.military_result_II = 0
        self.military_result_III = 0
        self.base_victory_points = 0
        self.dynamic_effects = []

        self.west_trade_costs = TradeCost()
        self.east_trade_costs = TradeCost()

    @property
    def state(self):
        self_dict = deepcopy(self.__dict__)
        self_dict.pop("name")
        self_dict.pop("player")
        self_dict.pop("dynamic_effects")
        return CityState(
            production=self.production,
            sellable_production=self.sellable_production,
            **self_dict,
        )

    def sample_card(self, logits: torch.Tensor, hand_tensor: torch.Tensor):
        # hand_tensor is used as a mask
        weights = hand_tensor * logits - (1 - hand_tensor) * 1e12
        probs = softmax(weights, dim=0)
        played_card_idx = torch.multinomial(probs, 1).item()
        return self.card_list[played_card_idx]

    def sample_trades(
        self,
        logits: torch.Tensor,
        west_sellable_production: SellableProduction,
        east_sellable_production: SellableProduction,
    ):
        # TODO split west and east
        coins_west = 0
        coins_east = 0

        gained_resources = Resources()

        trade_order = list(range(14))
        random.shuffle(trade_order)
        for idx in trade_order:
            if self.coins - coins_west - coins_east <= 0:
                break
            # check how many resources can possibly be bought
            resource = list(asdict(gained_resources).keys())[idx % 7]
            if idx < 7:
                max_buyable = west_sellable_production.max_amount(resource)
            else:
                max_buyable = east_sellable_production.max_amount(resource)
            if max_buyable == 0:
                continue

            # create mask to mask out amounts that cannot be bought
            mask = torch.ones(5)
            mask[max_buyable + 1 :] = 0
            # also mask out amounts that are too expensive
            if idx < 7:
                cost = getattr(self.west_trade_costs, resource)
            else:
                cost = getattr(self.east_trade_costs, resource)
            mask[int(cost * (self.coins - coins_west - coins_east)) + 1 :] = 0

            # sample how many resources are bought
            weights = mask * logits[idx] - (1 - mask) * 1e12
            probs = softmax(weights, dim=0)
            bought_amount = torch.multinomial(probs, 1).item()
            if bought_amount == 0:
                continue

            # update coin costs
            if idx < 7:
                coins_west += cost * bought_amount
            else:
                coins_east += cost * bought_amount

            gained_resources[resource] += bought_amount
            if idx < 7:
                west_sellable_production.remove(resource, bought_amount)
            else:
                east_sellable_production.remove(resource, bought_amount)
        return gained_resources, coins_west, coins_east

    # def sample_action(self, logits: torch.Tensor, card: Card, resources: Resources):
    #     TODO chain
    #     allowed_cards = Cards()
    # for card in cards:
    #     if card not in self.cards:
    #         allowed_cards[card.name] = True

    # weights = allowed_cards.as_tensor()
    #     remove cards that are already played
    #     afford_play = self.resources.is_affordable(card, resources)
    #     afford_wonder = self.resources.is_affordable(self.wonder_costs[0], resources)
    #     weights = torch.tensor([affordable, play_wonder, True]) # last is discarding
    #     probs = torch.nn.functional.softmax(logits * weights)
    #     action_idx = torch.multinomial(probs, 1).item()
    #     return action_idx

    def choose_play(
        self, hand: list[Card], west_city_state: CityState, east_city_state: CityState
    ):
        hand_card_list = CardList(**{c.name.replace(" ", "_"): True for c in hand})

        hand_tensor = hand_card_list.to_tensor()
        self_tensor = self.state.to_tensor()
        west_city_tensor = west_city_state.to_tensor()
        east_city_tensor = east_city_state.to_tensor()

        card_logits, trades_logits, action_logits = self.player(
            torch.cat([hand_tensor, self_tensor, west_city_tensor, east_city_tensor])
        )
        played_card = self.sample_card(card_logits, hand_tensor)
        played_trades = self.sample_trades(
            card_logits,
            deepcopy(west_city_state.sellable_production),
            deepcopy(east_city_state.sellable_production),
        )

    def apply_production_effect(self, effect: Effect):
        self.production += effect.production

    def apply_military_effect(self, effect: Effect):
        self.shields += effect.military.shields

    def apply_victory_point_effect(self, effect: Effect):
        if effect.victory_points.directions is None:
            self.dynamic_effects.append(effect)
        else:
            self.base_victory_points += effect.victory_points.amount

    def apply_science_effect(self, effect: Effect):
        self.__dict__[effect.science.symbol] += 1

    def apply_receive_coins_effect(
        self, effect: Effect, west_city_state: CityState, east_city_state: CityState
    ):
        if effect.receive_coins.directions is None:
            self.coins += effect.receive_coins.amount
        else:
            for direction in effect.receive_coins.directions:
                if direction == "west":
                    self.coins += (
                        effect.receive_coins.amount
                        * west_city_state[f"n_{effect.receive_coins.condition}"]
                    )
                if direction == "self":
                    self.coins += effect.receive_coins.amount * getattr(
                        self, f"n_{effect.receive_coins.condition}"
                    )
                if direction == "east":
                    self.coins += (
                        effect.receive_coins.amount
                        * east_city_state[f"n_{effect.receive_coins.condition}"]
                    )

    def apply_reduce_trade_cost_effect(self, effect: Effect):
        for resource in effect.reduce_trade_cost.resources:
            if "west" in effect.reduce_trade_cost.directions:
                self.west_trade_costs[resource] = 1
            if "east" in effect.reduce_trade_cost.directions:
                self.east_trade_costs[resource] = 1

    def apply_effect(
        self, effect: Effect, west_city_state: CityState, east_city_state: CityState
    ):
        if effect.production is not None:
            self.apply_production_effect(effect)
        if effect.military is not None:
            self.apply_military_effect(effect)
        if effect.victory_points is not None:
            self.apply_victory_point_effect(effect)
        if effect.science is not None:
            self.apply_science_effect(effect)
        if effect.receive_coins is not None:
            self.apply_receive_coins_effect(effect, west_city_state, east_city_state)
        if effect.reduce_trade_cost is not None:
            self.apply_reduce_trade_cost_effect(effect)

    def play(self, play: Play):
        card = card.play
        if play.action == Action.play_card:
            self.cards[play.card.name] = True
            self.__dict__[f"n_{play.card.colour}"] += 1
            self.apply_effect(card.effect)
            if card.cost["coins"] > 0:
                self.coins -= card.cost["coins"]
        elif play.action == Action.stage_wonder:
            self.wonder_stage += 1

            # no wonders cost coins
            self.apply_effect(self.wonder_effects[0])
            del self.wonder_effects[0]
        elif play.action == Action.discard:
            self.coins += 3

    def victory_points(self, west_city_state: CityState, east_city_state: CityState):
        victory_points = self.base_victory_points
        for effect in self.dynamic_effects:
            for direction in effect.victory_points.directions:
                if "," in effect.victory_points.condition:
                    conditions = effect.victory_points.condition.split(", ")
                else:
                    conditions = [effect.victory_points.condition]
                for condition in conditions:
                    if direction == "west":
                        victory_points += (
                            effect.victory_points.amount
                            * west_city_state[f"n_{condition}"]
                        )
                    if direction == "self":
                        victory_points += effect.victory_points.amount * getattr(
                            self, f"n_{condition}"
                        )
                    if direction == "east":
                        victory_points += (
                            effect.victory_points.amount
                            * east_city_state[f"n_{condition}"]
                        )
        return victory_points
