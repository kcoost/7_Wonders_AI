from typing import Any
from resources import Resources, Cost
from city import City


class Card:
    def __init__(
        self,
        age: str,
        n_players: int,
        name: str,
        chains: list[str],
        cost: dict[str, int],
    ):
        self.age = age
        self.name = name
        self.n_players = n_players
        self.cost = Cost(**cost)
        self.chains = chains


class ResourceCard(Card):
    def __init__(
        self,
        age: str,
        n_players: int,
        name: str,
        chains: list[str],
        cost: dict[str, int],
        effect: dict[str, int],
    ):
        super().__init__(age, n_players, name, chains, cost)

        self.resource_yields = []
        for resource, quantity in effect.items():
            self.resource_yields.append(Resources(**{resource: quantity}))

    def yield_resources(self):
        return self.resource_yields


class BrownCard(ResourceCard):
    colour = "Brown"

    def __repr__(self):
        return f"\033[33m{self.name}"


class GreyCard(ResourceCard):
    colour = "Grey"

    def __repr__(self):
        return f"\033[37m{self.name}"


class BlueCard(Card):
    colour = "Blue"

    def __init__(
        self,
        age: str,
        n_players: int,
        name: str,
        chains: list[str],
        cost: dict[str, int],
        effect: dict[str, int],
    ):
        super().__init__(age, n_players, name, chains, cost)
        self.victory_points = effect["Victory points"]

    def __repr__(self):
        return f"\033[34m{self.name}"


class RedCard(Card):
    colour = "Red"

    def __init__(
        self,
        age: str,
        n_players: int,
        name: str,
        chains: list[str],
        cost: dict[str, int],
        effect: dict[str, int],
    ):
        super().__init__(age, n_players, name, chains, cost)
        self.shields = effect["Shields"]
        assert self.age == self.shields

    def __repr__(self):
        return f"\033[31m{self.name}"


class GreenCard(Card):
    colour = "Green"

    def __init__(
        self,
        age: str,
        n_players: int,
        name: str,
        chains: list[str],
        cost: dict[str, int],
        effect: dict[str, str],
    ):
        super().__init__(age, n_players, name, chains, cost)
        self.symbol = effect["Symbol"]

    def __repr__(self):
        return f"\033[92m{self.name}"


class YellowCard(Card):
    colour = "Yellow"

    def __init__(
        self,
        age: str,
        n_players: int,
        name: str,
        chains: list[str],
        cost: dict[str, int],
        effect: dict[str, Any],
    ):
        super().__init__(age, n_players, name, chains, cost)

        self.effect = effect
        self.resource_yields = []
        if "Yield resources" in self.effect:
            for resource in effect["Yield resources"]:
                self.resource_yields.append(Resources(**{resource: 1}))

    def receive_coins(self, west_city: City, self_city: City, east_city: City):
        if "Receive coins" not in self.effect:
            return 0

        if "condition" not in self.effect["Receive coins"]:
            return self.effect["Receive coins"]["Amount"]

        coins = 0
        for direction in self.effect["Receive coins"]["Directions"]:
            if direction == "West":
                coins += west_city.count(self.effect["Receive coins"]["Condition"])
            if direction == "Self":
                coins += self_city.count(self.effect["Receive coins"]["Condition"])
            if direction == "East":
                coins += east_city.count(self.effect["Receive coins"]["Condition"])
        return coins

    def receive_victory_points(self, west_city: City, self_city: City, east_city: City):
        if "Receive victory points" not in self.effect:
            return 0

        victory_points = 0
        for direction in self.effect["Receive victory points"]["Directions"]:
            if direction == "West":
                victory_points += west_city.count(
                    self.effect["Receive victory points"]["Condition"]
                )
            if direction == "Self":
                victory_points += self_city.count(
                    self.effect["Receive victory points"]["Condition"]
                )
            if direction == "East":
                victory_points += east_city.count(
                    self.effect["Receive victory points"]["Condition"]
                )
        return victory_points

    def reduced_trading_costs(self, west_city: City, east_city: City):
        if "Trade" not in self.effect:
            return []

        resources = []
        # TODO
        for direction in self.effect["Trade"]["Directions"]:
            if direction == "West":
                resources += self.effect["Trade"]["Resources"]
            if direction == "East":
                resources += self.effect["Trade"]["Resources"]
        return resources

    def yield_resources(self):
        return self.resource_yields

    def __repr__(self):
        return f"\033[1;33m{self.name}"


class PurpleCard(Card):
    colour = "Purple"

    def __init__(
        self,
        age: str,
        n_players: int,
        name: str,
        chains: list[str],
        cost: dict[str, int],
        effect: dict[str, Any],
    ):
        super().__init__(age, n_players, name, chains, cost)
        self.effect = effect

    def receive_victory_points(self, west_city: City, self_city: City, east_city: City):
        if "Receive victory points" not in self.effect:
            return 0

        victory_points = 0
        for direction in self.effect["Receive victory points"]["Directions"]:
            if direction == "West":
                victory_points += west_city.count(
                    self.effect["Receive victory points"]["Condition"]
                )
            if direction == "Self":
                victory_points += self_city.count(
                    self.effect["Receive victory points"]["Condition"]
                )
            if direction == "East":
                victory_points += east_city.count(
                    self.effect["Receive victory points"]["Condition"]
                )
        return victory_points

    def all_symbols(self):
        return "Yield symbols" in self.effect["Effect"]

    def __repr__(self):
        return f"\033[35m{self.name}"


def build_card(
    age: str,
    n_players: int,
    colour: str,
    name: str,
    chains: list[str],
    cost: dict[str, int],
    effect: dict[str, int],
):
    cards = {
        "Brown": BrownCard,
        "Grey": GreyCard,
        "Blue": BlueCard,
        "Red": RedCard,
        "Green": GreenCard,
        "Yellow": YellowCard,
        "Purple": PurpleCard,
    }
    return cards[colour](age, n_players, name, chains, cost, effect)
