import random


class Policy:
    def __init__(self):
        pass

    def make_choice(self, options):
        pass


class RandomChoice(Policy):
    def make_choice(self, options):
        return random.randint(0, len(options)-1)
