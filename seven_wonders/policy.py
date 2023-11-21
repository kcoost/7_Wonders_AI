import random
import torch

random.seed(0)


class Policy:
    def __init__(self):
        pass

    def make_choice(self, available_cards):
        pass


class RandomChoice(Policy):
    def make_choice(self, available_cards):
        names, weights = available_cards.as_tensor()
        if weights.sum() == 0:
            return "Discard", "TODO"
        return "Action", names[torch.multinomial(weights, 1).item()]
