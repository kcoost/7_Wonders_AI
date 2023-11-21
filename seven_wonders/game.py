from pathlib import Path
import random

import jsonlines
from .cards import Card, build_card

random.seed(0)
from common import *
from .helpers import (
    init_decks,
    score_military,
    score_blue,
    score_science,
    score_yellow,
    score_purple,
)
from .Players import Player
import logger
from .policy import StupidAI
from .utils import CyclicList

class Decks:
    def __init__(self, player_count: int, age_I_cards: list[Card], age_II_cards: list[Card], age_III_cards: list[Card]):
        self.age_I_cards = age_I_cards
        self.age_II_cards = age_II_cards
        self.age_III_cards = age_III_cards

    def deal_hands(self, turn):
        return []

    def update_cards(self):
        # remove card
        # rotate


class GameState:
    def __init__(self, players: list[Player]):
        self.players = CyclicList(players)
        self.player_count = len(players)
        self.decks = self.build_decks(self.player_count)
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

        return Decks(player_count, age_I_cards, age_II_cards, age_III_cards)

    def deal_age_cards(self, age):
        cards = self.ages[age][0:]
        p = 0
        for i in range(self.player_count):
            self.decks[i] = []
        while len(cards):
            self.decks[p].append(cards[0])
            p += 1
            p %= self.player_count
            cards = cards[1:]

    def left_player(self, player_id):
        return self.players[player_id - 1]

    def right_player(self, player_id):
        return self.players[player_id + 1]

    def play_turn(self, offset):
        for i in range(self.player_count):
            player = self.players[i]
            west_player = self.left_player(i)
            east_player = self.right_player(i)
            deckid = (i + offset) % self.player_count
            # This loop is actually wrong.
            # Everyone should choose the card they will play, server
            # validates the move is legal, then each player plays the card
            # Then each player adds the new card to their board
            while True:
                action, card = player.play_hand(
                    self.decks[deckid], west_player, east_player
                )
                if action == ACTION_PLAYCARD:
                    can_buy = False
                    # see if the player can buy the card
                    if player.can_build_with_chain(card):
                        can_buy = True
                        self.logger.log_buy_card_with_chain(player, card)
                    else:
                        buy_options = player.buy_card(card, west_player, east_player)
                        if len(buy_options) == 0:
                            continue
                        self.logger.log_buy_card(player, card, buy_options[0])
                        can_buy = True
                        player.money -= buy_options[0].total_cost
                        east_player.money += buy_options[0].east_cost
                        west_player.money += buy_options[0].west_cost
                    if can_buy:
                        card.play(player, west_player, east_player)
                        player.get_cards().append(card)
                        break
                elif action == ACTION_DISCARD:
                    self.logger.log_action(player, action, card)
                    self.discard_pile.append(card)
                    player.money += 3
                    break
                elif action == ACTION_STAGEWONDER:
                    self.logger.log_action(player, action, card)
                    # make sure we can do that
                    break
            self.decks[deckid].remove(card)

    def get_score(self):
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

    def game_loop(self):
        for age in range(3):
            self.logger.log_age_header(age)
            self.deal_age_cards(age)
            offset = 0
            while len(self.decks[0]) > 1:
                self.play_turn(offset)
                offset = (
                    offset + [1, self.player_count - 1, 1][age]
                ) % self.player_count
            # everyone discards the last card
            for p in range(self.player_count):
                self.discard_pile.append(self.decks[p][0])

            # score military
            for p in range(self.player_count):
                west = self.left_player(p)
                east = self.right_player(p)
                player = self.players[p]
                player_strength, opponent_strength, score = score_military(
                    player, west, age
                )
                self.logger.log_military_battle(
                    player.get_name(),
                    player_strength,
                    west.get_name(),
                    opponent_strength,
                    score,
                )
                self.players[p].military.append(score)
                player_strength, opponent_strength, score = score_military(
                    player, east, age
                )
                self.logger.log_military_battle(
                    player.get_name(),
                    player_strength,
                    east.get_name(),
                    opponent_strength,
                    score,
                )
                self.players[p].military.append(score)
        self.get_score()

        logfile = open("logfile.txt", "w")
        self.logger.dump(logfile)
        logfile.close()


def run_game():
    Alice = Player("Alice", StupidAI())
    Bob = Player("Bob", StupidAI())
    Charlie = Player("Charlie", StupidAI())

    game = GameState([Alice, Bob, Charlie])
    game.game_loop()
