from itertools import product
from .resources import Production
from .card import Card

class City:
    def __init__(self):
        self.played_cards = []
        self.resource_production = [Production(Clay=1)]

    def update_resource_production(self, card: Card):
        assert card.colour in ["Brown", "Grey", "Yellow"]

        # create all new possible resource productions
        resource_productions = []
        for production_1, production_2 in product(self.resource_production, card.resource_production):
            combined_production = production_1 + production_2
            if combined_production not in resource_productions:
                resource_productions.append(combined_production)

        # TODO: remove cards that have
        # # remove low productions
        # best_resource_productions = []
        # for production in updated_resource_production:
        #     if any(p > production for p in best_resource_productions):
        #         best_resource_productions
        self.resource_production = resource_productions

    def is_affordable(self, card: Card):
        for resources in self.resource_production:
            if card.cost <= resources:
                return True
            # TODO trading
        return False
