from pathlib import Path
import random
import pandas as pd

import jsonlines

random.seed(0)
from collections import deque

from common import CARDS_BROWN, CARDS_GREY,CARDS_BLUE,CARDS_GREEN, CARDS_RED, CARDS_YELLOW, CARDS_PURPLE, Colour,SCIENCE_COMPASS, SCIENCE_GEAR, SCIENCE_TABLET
from . import Cards





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
        if c.colour == CARDS_GREEN:
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

    for c in [c for c in player.get_cards() if c.colour == CARDS_RED]:
        my_strength += c.get_strength()
    for c in [c for c in opponent.get_cards() if c.colour == CARDS_RED]:
        their_strength += c.get_strength()

    if my_strength > their_strength:
        points = [1, 3, 5][age]
    elif my_strength < their_strength:
        points = -1
    return (my_strength, their_strength, points)


def score_blue(player):
    score = 0
    for c in [c for c in player.get_cards() if c.colour == CARDS_BLUE]:
        score += c.score()
    return score


def score_yellow(player, west_player, east_player):
    score = 0
    for c in [c for c in player.get_cards() if c.colour == CARDS_YELLOW]:
        score += c.score(player, west_player, east_player)
    return score


def score_purple(player, west_player, east_player):
    score = 0
    for c in [c for c in player.get_cards() if c.colour == CARDS_PURPLE]:
        score += c.score(player, west_player, east_player)
    return score
