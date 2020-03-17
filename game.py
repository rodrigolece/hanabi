import itertools
import textwrap
import numpy as np

from player import Player
from card import Card
from table import Table


class Hanabi(object):
    # table : Table
    # stack : list(Card)
    # discarded : list(Card)
    # players : list(Player)
    # current_player : Player
    # round : int
    # clues : int
    # lifes : int

    def __init__(self, nb_players, seed=42):
        self.nb_players = nb_players
        self.round = 0
        self.clues = 8
        self.lifes = 3
        self.table = Table()

        self._rng = np.random.RandomState(seed)

        colours = ['red', 'blue', 'green', 'yellow', 'white']
        numbers = [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]

        cards = [Card(c, n) for (c, n) in itertools.product(colours, numbers)]
        self.stack = self._rng.permutation(cards).tolist()
        self.discarded = []

        # TODO: check in the rules if numbers are right below
        rules_dict = dict([(2, 6), (3, 5), (4, 5), (5, 4)])
        nb_to_deal = rules_dict[self.nb_players]

        self.players = []

        for i in range(self.nb_players):
            player = Player(i)
            self.players.append(player)
            self.deal_cards(player, nb_to_deal)

        to_play = self.round % self.nb_players
        self.current_player = self.players[to_play]

    def __str__(self):
        s = f"""
            Hanabi game with {self.nb_players} players at round {self.round}
             - Remaining lifes: {self.lifes}
             - Remaining clues: {self.clues}"""

        return textwrap.dedent(s)

    def deal_cards(self, player, nb_cards):
        for i in range(nb_cards):
            card = self.stack.pop()
            player.hand.append(card)

        return None

    def next_player(self):
        self.round += 1
        to_play = self.round % self.nb_players
        self.current_player = self.players[to_play]

        return None
