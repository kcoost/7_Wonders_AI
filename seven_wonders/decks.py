import random
import jsonlines
from pathlib import Path
from .cards import Card

#random.seed(0)

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

    def remove_cards(self, card_names: list[str]):
        for i, card_name in enumerate(card_names):
            hand_card_names = [c.name for c in self.hands[i]]
            removed_card_idx = hand_card_names.index(card_name)
            del self.hands[i][removed_card_idx]

def build_decks(player_count):
    age_I_cards = []
    age_II_cards = []
    age_III_cards = []
    purple_cards = []
    with jsonlines.open(Path(__file__).parent / "cards_information.jsonl") as file:
        for card_data in file:
            if player_count < card_data["n_players"]:
                continue
            if card_data["age"] == "I":
                age_I_cards.append(Card(**card_data))
            elif card_data["age"] == "II":
                age_II_cards.append(Card(**card_data))
            elif card_data["colour"] == "purple":
                purple_cards.append(Card(**card_data))
            elif card_data["age"] == "III":
                age_III_cards.append(Card(**card_data))

    random.shuffle(age_I_cards)
    random.shuffle(age_II_cards)
    random.shuffle(purple_cards)
    age_III_cards += purple_cards[:player_count + 2]
    random.shuffle(age_III_cards)

    return Deck(player_count, "clockwise", age_I_cards), Deck(player_count, "anti_clockwise", age_II_cards), Deck(player_count, "clockwise", age_III_cards)
