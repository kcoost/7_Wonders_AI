from .game_logger import GameLogger
from .decks import build_decks
from .plays import Play
from .city_base import City


class GameState:
    def __init__(self, cities: list[City]):
        super().__init__()
        self.cities = cities
        self.city_count = len(cities)
        self.deck_I, self.deck_II, self.deck_III = build_decks(self.city_count)
        self.logger = GameLogger()

    def choose_plays(self, age: str):
        plays = []

        deck = getattr(self, f"deck_{age}")
        hands = deck.hands
        for i in range(self.city_count):
            hand = hands[i]
            west_city_state = self.cities[(i + 1) % self.city_count].state
            east_city_state = self.cities[(i - 1) % self.city_count].state
            play = self.cities[i].choose_play(hand, west_city_state, east_city_state)

            self.logger.choose_play(self.cities[i].name, play)
            plays.append(play)
        return plays

    def play(self, plays: list[Play]):
        for i, play in enumerate(plays):
            self.cities[i].play(play)

    def military_battles(self):
        for i in range(self.city_count):
            west_city_shields = self.cities[(i + 1) % self.city_count].shields
            east_city_shields = self.cities[(i - 1) % self.city_count].shields
            results = self.cities[i].military_battle(west_city_shields, east_city_shields)
            self.logger.military_battle(results)

    def play_game(self):
        self.logger.start_game(self.cities)

        for age in ["I", "II", "III"]:
            self.logger.start_age(age)

            for turn in range(1, 7):
                self.logger.start_turn(turn)

                plays = self.choose_plays(age)

                # update deck
                getattr(self, f"deck_{age}").remove_cards([p.card.name for p in plays])
                getattr(self, f"deck_{age}").rotate_hands()

                self.play(plays)

            self.military_battles()

        winning_score = 0
        for i in range(self.city_count):
            west_city_state = self.cities[(i + 1) % self.city_count].state
            east_city_state = self.cities[(i - 1) % self.city_count].state
            score = self.cities[i].military_battle(west_city_state, east_city_state)

            self.logger.game_results(winner, score)

            if score > winning_score:
                winning_score = score
                winner = self.cities[i].name

        self.logger.winner(winner)
