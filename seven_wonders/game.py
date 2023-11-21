import random
import jsonlines
import logger

from pathlib import Path

from .card import Card, build_card
from .policy import RandomChoice
from .utils import CyclicList
from .player import Player
from .city import City


class Deck:
    def __init__(self, player_count: int, rotation_direction: str, cards: list[Card]):
        self.rotation_direction = rotation_direction
        initial_hand_size = len(cards) // player_count
        self.hands = []
        for i in range(len(cards) // initial_hand_size):
            self.hands.append(cards[i*initial_hand_size:(i+1)*initial_hand_size])

    def rotate_hands(self):
        # TODO check logic
        if self.rotation_direction == "clockwise":
            self.hands = self.hands[1:] + [self.hands[0]]
        else:
            self.hands = [self.hands[-1]] + self.hands[:-1]

    def remove_cards(self, cards: list[Card]):
        for i, card in enumerate(cards):
            pass
            #self.hands[i].pop(card)


class GameState:
    def __init__(self, players: list[Player]):
        self.players = CyclicList(players)
        self.player_count = len(players)
        self.deck_I, self.deck_II, self.deck_III = self.build_decks(self.player_count)
        # self.discard_pile = []
        self.logger = logger.Logger()

    @staticmethod
    def build_decks(player_count):
        age_I_cards = []
        age_II_cards = []
        age_III_cards = []
        purple_cards = []
        with jsonlines.open(Path(__file__).parent / "cards_information.jsonl") as file:
            for card_data in file:
                if player_count > card_data["N_players"]:
                    continue
                if card_data["Age"] == "I":
                    age_I_cards.append(build_card(**card_data))
                elif card_data["Age"] == "II":
                    age_II_cards.append(build_card(**card_data))
                elif card_data["Colour"] == "Purple":
                    purple_cards.append(build_card(**card_data))
                elif card_data["Age"] == "III":
                    age_III_cards.append(build_card(**card_data))

        random.shuffle(age_I_cards)
        random.shuffle(age_II_cards)
        random.shuffle(purple_cards)
        age_III_cards += purple_cards[:player_count + 2]
        random.shuffle(age_III_cards)

        return Deck(player_count, "clockwise", age_I_cards), Deck(player_count, "anti_clockwise", age_II_cards), Deck(player_count, "clockwise", age_III_cards)

    def play_turn(self, age: str):
        played_cards = []
        deck = getattr(self, f"deck_{age}")
        hands = deck.hands
        for i in range(self.player_count):
            hand = hands[i]
            #west_city = self.players[(i + 1) % self.player_count].city
            #east_city = self.players[(i - 1) % self.player_count].city
            available_cards = self.players[i].actions(hand)#, west_city, east_city)
            action, played_card = self.players[i].make_choice(available_cards)
            played_cards.append(played_card)
        print("Cards played:", played_cards)

        deck.remove_cards(played_cards)
        deck.rotate_hands()

        for i, played_card in enumerate(played_cards):
            self.players[i].play_card(action, played_card)

    def update_scores(self):
        pass

    def play_game(self):
        for age in ["I", "II", "III"]:
            for turn in range(6):
                self.play_turn(age)
            self.update_scores()

    def get_score(self):
        return
        for i in range(self.player_count):
            player = self.players[i]
            west = self.left_player(i)
            east = self.right_player(i)
            bluescore = score_blue(player)
            _, greenscore = score_science(player)
            redscore = 0
            for military in player.military:
                redscore += military
            moneyscore = player.money / 3
            yellowscore = score_yellow(player, west, east)
            purplescore = score_purple(player, west, east)
            totalscore = (
                bluescore
                + greenscore
                + redscore
                + moneyscore
                + yellowscore
                + purplescore
            )
            text = (
                "Final score: Blue: %d, Green: %d, red: %d, yellow: %d, purple: %d, $: %d, total: %d"
                % (
                    bluescore,
                    greenscore,
                    redscore,
                    yellowscore,
                    purplescore,
                    moneyscore,
                    totalscore,
                )
            )
            self.logger.log_freetext(player.get_name() + " " + text)


def run_game():
    Alice = Player("Alice", City(), RandomChoice())
    Bob = Player("Bob", City(), RandomChoice())
    Charlie = Player("Charlie", City(), RandomChoice())

    game = GameState([Alice, Bob, Charlie])
    game.play_game()
