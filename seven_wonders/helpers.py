from pathlib import Path
import random
import pandas as pd

import jsonlines

random.seed(0)
from collections import deque

from common import *
from . import Cards


def build_card(colour, name, age, cost, players, infostr):
    cardclasses = {
        CARDS_BROWN: Cards.BrownCard,
        CARDS_GREY: Cards.GreyCard,
        CARDS_BLUE: Cards.BlueCard,
        CARDS_GREEN: Cards.GreenCard,
        CARDS_RED: Cards.RedCard,
        CARDS_YELLOW: Cards.YellowCard,
        CARDS_PURPLE: Cards.YellowCard,
    }

    if not colour in cardclasses:
        return None

    card = cardclasses[colour](name, age, cost, players)

    if card != None and card.parse_infotext(infostr):
        if colour == CARDS_PURPLE:
            card.colour = CARDS_PURPLE
        return card

    print("Error loading card:", name)
    return None


def init_decks(player_count):
    data = pd.read_json(Path(__file__).parent / "cards_information.jsonl", lines=True)
    data = data[data["N_players"] <= player_count]

    cards = []
    for _, row in data.iterrows():
        c = build_card(
            row["Colour"],
            row["Name"],
            row["Age"],
            row["Cost"],
            row["N_players"],
            row["Text"],
        )
        if c:
            c.parse_chains(row["Prebuilt"], row["Postbuilt"])
            cards.append(c)

    age_1 = [c for c in cards if c.age == 1]
    age_2 = [c for c in cards if c.age == 2]
    age_3 = [c for c in cards if c.age == 3 and c.get_colour() != CARDS_PURPLE]
    purple = [c for c in cards if c.age == 3 and c.get_colour() == CARDS_PURPLE]
    random.shuffle(age_1)
    random.shuffle(age_2)
    random.shuffle(purple)
    age_3 += purple[0 : player_count + 2]
    random.shuffle(age_3)

    ages = [age_1, age_2, age_3]
    return cards, ages


def calc_science_score(compass, gear, tablets):
    counts = sorted([compass, gear, tablets], reverse=True)
    total = 0
    for i in range(3):
        total += counts[i] * counts[i]
    return 7 * counts[2] + total


def find_best_score(compass, gear, tablets, choice):
    if len(choice) == 0:
        score = calc_science_score(compass, gear, tablets)
        return ((compass, gear, tablets), score)
    scores = []
    if SCIENCE_COMPASS in choice[0]:
        scores.append(find_best_score(compass + 1, gear, tablets, choice[1:]))
    if SCIENCE_GEAR in choice[0]:
        scores.append(find_best_score(compass, gear + 1, tablets, choice[1:]))
    if SCIENCE_TABLET in choice[0]:
        scores.append(find_best_score(compass, gear, tablets + 1, choice[1:]))
    return sorted(scores, key=lambda score: score[1], reverse=True)[0]


def score_science(player):
    count = {}
    count[SCIENCE_COMPASS] = 0
    count[SCIENCE_GEAR] = 0
    count[SCIENCE_TABLET] = 0
    choice_cards = []  # An array tuples of available choices
    for c in player.get_cards():
        if c.get_colour() == CARDS_GREEN:
            count[c.get_info()] += 1
        elif c.is_science_card():
            choice_cards.append((c.provisions))

    return find_best_score(
        count[SCIENCE_COMPASS], count[SCIENCE_GEAR], count[SCIENCE_TABLET], choice_cards
    )


def score_military(player, opponent, age):
    my_strength = 0
    their_strength = 0
    points = 0

    for c in [c for c in player.get_cards() if c.get_colour() == CARDS_RED]:
        my_strength += c.get_strength()
    for c in [c for c in opponent.get_cards() if c.get_colour() == CARDS_RED]:
        their_strength += c.get_strength()

    if my_strength > their_strength:
        points = [1, 3, 5][age]
    elif my_strength < their_strength:
        points = -1
    return (my_strength, their_strength, points)


def score_blue(player):
    score = 0
    for c in [c for c in player.get_cards() if c.get_colour() == CARDS_BLUE]:
        score += c.score()
    return score


def score_yellow(player, west_player, east_player):
    score = 0
    for c in [c for c in player.get_cards() if c.get_colour() == CARDS_YELLOW]:
        score += c.score(player, west_player, east_player)
    return score


def score_purple(player, west_player, east_player):
    score = 0
    for c in [c for c in player.get_cards() if c.get_colour() == CARDS_PURPLE]:
        score += c.score(player, west_player, east_player)
    return score
