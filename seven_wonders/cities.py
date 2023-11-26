from .city_base import City
from .resources import Cost, Production, SellableProduction
from .effect import Effect

# See https://thethoughtfulgamer.com/2020/05/09/analyzing-the-wonders-in-7-wonders/


class AlexandriaA(City):
    side = "A"
    production = Production(glass=1)
    sellable_production = SellableProduction(glass=1)
    wonder_costs = (Cost(stone=2), Cost(ore=2), Cost(glass=2))
    wonder_effects = (
        Effect(victory_points={"amount": 3}),
        Effect(production={"any_raw_material": 1}),
        Effect(victory_points={"amount": 7}),
    )


class AlexandriaB(City):
    side = "B"
    production = Production(glass=1)
    sellable_production = SellableProduction(glass=1)
    wonder_costs = (Cost(clay=2), Cost(wood=2), Cost(stone=3))
    wonder_effects = (
        Effect(production={"any_raw_material": 3}),
        Effect(production={"any_good": 1}),
        Effect(victory_points={"amount": 7}),
    )


# class Babylon(City):
#     ...


class EphesosA(City):
    side = "A"
    production = Production(papyrus=1)
    sellable_production = SellableProduction(papyrus=1)
    wonder_costs = (Cost(stone=2), Cost(wood=2), Cost(papyrus=2))
    wonder_effects = (
        Effect(victory_points={"amount": 3}),
        Effect(receive_coins={"amount": 9}),
        Effect(victory_points={"amount": 7}),
    )


class EphesosB(City):
    side = "B"
    production = Production(papyrus=1)
    sellable_production = SellableProduction(papyrus=1)
    wonder_costs = (Cost(stone=2), Cost(wood=2), Cost(papyrus=1, loom=1, glass=1))
    wonder_effects = (
        Effect(victory_points={"amount": 2}, receive_coins={"amount": 4}),
        Effect(victory_points={"amount": 3}, receive_coins={"amount": 4}),
        Effect(victory_points={"amount": 5}, receive_coins={"amount": 4}),
    )


class GizaA(City):
    side = "A"
    production = Production(stone=1)
    sellable_production = SellableProduction(stone=1)
    wonder_costs = (Cost(stone=2), Cost(wood=3), Cost(stone=4))
    wonder_effects = (
        Effect(victory_points={"amount": 3}),
        Effect(victory_points={"amount": 5}),
        Effect(victory_points={"amount": 7}),
    )


class GizaB(City):
    side = "B"
    production = Production(stone=1)
    sellable_production = SellableProduction(stone=1)
    wonder_costs = (Cost(wood=2), Cost(stone=3), Cost(clay=3), Cost(stone=4, papyrus=1))
    wonder_effects = (
        Effect(victory_points={"amount": 3}),
        Effect(victory_points={"amount": 5}),
        Effect(victory_points={"amount": 5}),
        Effect(victory_points={"amount": 7}),
    )


# class Halicarnassus(City):
#     ...

# class Olympia(City):
#     ...


class RhodesA(City):
    side = "A"
    production = Production(ore=1)
    sellable_production = SellableProduction(ore=1)
    wonder_costs = (Cost(wood=2), Cost(clay=3), Cost(ore=4))
    wonder_effects = (
        Effect(victory_points={"amount": 3}),
        Effect(military={"shields": 2}),
        Effect(victory_points={"amount": 7}),
    )


class RhodesB(City):
    side = "B"
    production = Production(ore=1)
    sellable_production = SellableProduction(ore=1)
    wonder_costs = (Cost(stone=3), Cost(ore=4))
    wonder_effects = (
        Effect(
            victory_points={"amount": 3},
            receive_coins={"amount": 3},
            military={"shields": 1},
        ),
        Effect(
            victory_points={"amount": 4},
            receive_coins={"amount": 4},
            military={"shields": 1},
        ),
    )
