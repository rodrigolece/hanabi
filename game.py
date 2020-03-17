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
            player.hand_info["numbers"].append(None)
            player.hand_info["colours"].append(None)

        return None

    def next_player(self):
        self.round += 1
        to_play = self.round % self.nb_players
        self.current_player = self.players[to_play]
        print("\nCurrent player is player {}".format(to_play))

        return None

    # redundancy in the functions below? being in game and player?

    # should you have to specify which player does this? or should it always be "self.current player"
    def pickup_card(self, player):
        card = self.stack.pop()
        player.pickup(card)

        return None


    def discard_card(self, player, card_num):
        self.clues+=1
        discarded = player.discard(card_num)
        self.table.discarded_stack.append(discarded)
        self.pickup_card(player)
        return None


    def play_card(self, player, card_num):
        stack_name = f'{player.hand[card_num].colour}_stack'
        stack = getattr(self.table, stack_name, None)
        card = player.play(card_num)

        if len(stack) > 0:  # the stack has cards
            top_card = stack[-1]
            if card.number == top_card.number + 1:
                stack.append(card)
            else:
                print("life lost")
                self.discard_card(player, card_num)
                self.clues -=1 # this is so hacky. At the moment using the discard function adds a clue
                self.lifes -=1
                if self.lifes ==0:
                    print(" YOU LOSE")
                    exit()

        else:
            if card.number == 1:
                stack.append(card)
            else:
                print("life lost")
                self.discard_card(player, card_num)
                self.clues -=1 # this is so hacky
                self.lifes -=1
                if self.lifes ==0:
                    print(" YOU LOSE")
                    exit()

        self.pickup_card(player)

        return None

    def give_hint(self, to_player, card_num, info):
        if self.clues>0:
            if info in ['red', 'blue', 'green', 'yellow', 'white']:
                hint_type = 'colours'
            elif info in [1,2,3,4,5]:
                hint_type= 'numbers'
            to_player.hand_info[hint_type][card_num]=info
            self.clues-=1
        else:
            print("\n No hints to left to give. Discard or play")
        return None
