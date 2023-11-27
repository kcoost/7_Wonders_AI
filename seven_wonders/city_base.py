from copy import deepcopy
import random
import torch
from torch.nn.functional import softmax
from dataclasses import asdict, dataclass
from .scores import compute_green_score
from .players import Player
from .city_state import CityState, CardList
from .plays import Play, Trade
from .action import Action
from .effect import Effect
from .resources import Production, TradeCost, Cost, Resources, SellableProduction
from .cards import Card

#random.seed(0)
#torch.manual_seed(0)


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
        self.scripts = 0
        self.any_symbols = 0

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
        if "production" in self_dict:
            self_dict.pop("production")
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
        return self.card_list[played_card_idx], probs[played_card_idx]

    def sample_trades(
        self,
        logits: torch.Tensor,
        west_sellable_production: SellableProduction,
        east_sellable_production: SellableProduction,
    ):
        # TODO split west and east
        coins_west = 0
        coins_east = 0

        gained_resources_west = Resources()
        gained_resources_east = Resources()

        trade_order = list(range(14))
        random.shuffle(trade_order)
        for idx in trade_order:
            if self.coins - coins_west - coins_east <= 0:
                break
            # check how many resources can possibly be bought
            resource = list(asdict(gained_resources_west).keys())[idx % 7]
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
                gained_resources_west.add(resource, bought_amount)
            else:
                coins_east += cost * bought_amount
                gained_resources_east.add(resource, bought_amount)

            if idx < 7:
                west_sellable_production.remove(resource, bought_amount)
            else:
                east_sellable_production.remove(resource, bought_amount)
        return gained_resources_west, gained_resources_east, coins_west, coins_east

    def sample_action(self, logits: torch.Tensor, card: Card, bought_resources: Resources, available_coins: int):
        # afford card
        total_resources = self.production + bought_resources
        if card.is_chained(self.card_list):
            affordable = True
            spent_coins = 0
        elif total_resources.can_afford(card.base_cost) and card.base_cost.coins <= available_coins:
            affordable = True
            spent_coins = card.base_cost.coins
        else:
            affordable = False
            spent_coins = 0

        # afford wonder
        if total_resources.can_afford(self.wonder_costs[self.n_wonder]):
            if self.n_wonder == len(self.wonder_costs) - 1:
                wonder_affordable = False
            else:
                wonder_affordable = True
        else:
            wonder_affordable = False

        can_discard = True

        mask = torch.Tensor([affordable, wonder_affordable, can_discard])
        weights = mask * logits - (1 - mask) * 1e12
        probs = softmax(weights, dim=0)
        action_idx = torch.multinomial(probs, 1).item()
        if action_idx == 0:
            return Action.play_card, spent_coins, probs[action_idx]
        elif action_idx == 1:
            return Action.stage_wonder, 0, probs[action_idx]
        elif action_idx == 2:
            return Action.discard, -3, probs[action_idx]

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
        played_card_name, prob_card = self.sample_card(card_logits, hand_tensor)
        played_card = [c for c in hand if c.name.replace(" ", "_") == played_card_name][0]
        gained_resources_west, gained_resources_east, coins_west, coins_east = self.sample_trades(
            trades_logits,
            deepcopy(west_city_state.sellable_production),
            deepcopy(east_city_state.sellable_production),
        )
        played_action, spent_coins, prob_action = self.sample_action(action_logits, played_card, gained_resources_west + gained_resources_east, self.coins - coins_west - coins_east)
        return Play(card=played_card,
                    action=played_action,
                    spent_coins=spent_coins,
                    trade_west=Trade(coins=coins_west, **asdict(gained_resources_west)),
                    trade_east=Trade(coins=coins_east, **asdict(gained_resources_east))), prob_card, prob_action

    def apply_production_effect(self, effect: Effect):
        self.production += effect.production

    def apply_military_effect(self, effect: Effect):
        self.shields += effect.military.shields

    def apply_victory_point_effect(self, effect: Effect):
        if effect.victory_points.directions is not None:
            self.dynamic_effects.append(effect)
        else:
            self.base_victory_points += effect.victory_points.amount

    def apply_science_effect(self, effect: Effect):
        self.__dict__[f"{effect.science.symbol}s"] += 1

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
                        * getattr(west_city_state, f"n_{effect.receive_coins.condition}")
                    )
                if direction == "self":
                    self.coins += effect.receive_coins.amount * getattr(
                        self, f"n_{effect.receive_coins.condition}"
                    )
                if direction == "east":
                    self.coins += (
                        effect.receive_coins.amount
                        * getattr(east_city_state, f"n_{effect.receive_coins.condition}")
                    )

    def apply_reduce_trade_cost_effect(self, effect: Effect):
        for resource in effect.reduce_trade_cost.resources:
            if "west" in effect.reduce_trade_cost.directions:
                setattr(self.west_trade_costs, resource, 1)
            if "east" in effect.reduce_trade_cost.directions:
                setattr(self.east_trade_costs, resource, 1)

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

    def play(self, play: Play, west_city_state: CityState, east_city_state: CityState, coins: int):
        card = play.card
        self.coins += coins
        if play.action == Action.play_card:
            setattr(self.card_list, play.card.name, True)
            self.__dict__[f"n_{play.card.colour}"] += 1
            self.apply_effect(card.effect, west_city_state, east_city_state)
        elif play.action == Action.stage_wonder:
            self.n_wonder += 1

            # no wonders cost coins
            self.apply_effect(self.wonder_effects[0])
            del self.wonder_effects[0]

    def military_battle(self, age: str, west_city_shields: int, east_city_shields: int):
        defeats = int(west_city_shields > self.shields) + int(east_city_shields > self.shields)
        self.n_military_defeat += defeats

        wins = int(west_city_shields < self.shields) + int(east_city_shields < self.shields)
        setattr(self, f"military_result_{age}", -defeats + (2*len(age)-1)*wins)

        if west_city_shields < self.shields:
            west_result = 2*len(age)-1
        elif west_city_shields > self.shields:
            west_result = -1
        else:
            west_result = 0

        if east_city_shields < self.shields:
            east_result = 2*len(age)-1
        elif east_city_shields > self.shields:
            east_result = -1
        else:
            east_result = 0
        return [west_result, east_result]

    def victory_points(self, west_city_state: CityState, east_city_state: CityState):
        # blue and wonder results
        victory_points = self.base_victory_points

        # coins
        victory_points += self.coins // 3

        # military results
        victory_points += self.military_result_I
        victory_points += self.military_result_II
        victory_points += self.military_result_III

        # science results
        victory_points += compute_green_score(self.state)
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
                            * getattr(west_city_state, f"n_{condition}")
                        )
                    if direction == "self":
                        victory_points += effect.victory_points.amount * getattr(
                            self, f"n_{condition}"
                        )
                    if direction == "east":
                        victory_points += (
                            effect.victory_points.amount
                            * getattr(east_city_state, f"n_{condition}")
                        )
        return victory_points
