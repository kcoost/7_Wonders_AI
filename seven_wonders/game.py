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
        probs_card = []
        probs_action = []
        rewards = []

        plays = []

        deck = getattr(self, f"deck_{age}")
        hands = deck.hands
        for i in range(self.city_count):
            hand = hands[i]
            west_city_state = self.cities[(i + 1) % self.city_count].state
            east_city_state = self.cities[(i - 1) % self.city_count].state
            play, prob_card, prob_action = self.cities[i].choose_play(hand, west_city_state, east_city_state)

            self.logger.choose_play(self.cities[i].name, play)
            plays.append(play)
            if i == 0:
                probs_card = prob_card
                probs_action = prob_action
                rewards = self.cities[i].victory_points(west_city_state, east_city_state)
        return plays, probs_card, probs_action, rewards

    def play(self, plays: list[Play]):
        for i, play in enumerate(plays):
            west_city_state = self.cities[(i + 1) % self.city_count].state
            east_city_state = self.cities[(i - 1) % self.city_count].state

            coins = plays[(i + 1) % self.city_count].trade_east.coins + plays[(i - 1) % self.city_count].trade_west.coins - play.spent_coins
            self.cities[i].play(play, west_city_state, east_city_state, coins)

    def military_battles(self, age: str):
        for i in range(self.city_count):
            west_city_shields = self.cities[(i + 1) % self.city_count].shields
            east_city_shields = self.cities[(i - 1) % self.city_count].shields
            results = self.cities[i].military_battle(age, west_city_shields, east_city_shields)
            self.logger.military_battle(self.cities[i].name, results)

    def play_game(self):
        probs_card = []
        probs_action = []
        rewards = []

        self.logger.start_game(self.cities)

        for age in ["I", "II", "III"]:
            self.logger.start_age(age)

            for turn in range(1, 8):
                self.logger.start_turn(turn)

                plays, prob_card, prob_action, reward = self.choose_plays(age)
                probs_card.append(prob_card)
                probs_action.append(prob_action)
                rewards.append(reward)

                # update deck
                getattr(self, f"deck_{age}").remove_cards([p.card.name for p in plays])
                getattr(self, f"deck_{age}").rotate_hands()

                self.play(plays)

            self.military_battles(age)

        winning_score = 0
        for i in range(self.city_count):
            west_city_state = self.cities[(i + 1) % self.city_count].state
            east_city_state = self.cities[(i - 1) % self.city_count].state
            score = self.cities[i].victory_points(west_city_state, east_city_state)

            self.logger.game_results(self.cities[i].name, score)

            if score > winning_score:
                winning_score = score
                winner = self.cities[i].name

        self.logger.winner(winner, winning_score)
        return winner, probs_card, probs_action, rewards
