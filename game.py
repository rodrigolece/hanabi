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

    def __init__(self, nb_players, id_game=0, seed=42):
        # Below is used in online games
        self._num_connections = 1  # a game is initialised when there is 1 connection
        self._ready = False
        self._finished = None
        self._id_game = id_game

        self.nb_players = nb_players
        self.round = 0
        self.clues = 8
        self.lifes = 3
        self.table = Table()

        self._rng = np.random.RandomState(seed)
        self._endgame_flag = False
        self._endgame_count = self.nb_players

        colours = ['red', 'blue', 'green', 'yellow', 'white']
        numbers = [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]

        cards = [Card(c, n) for (c, n) in itertools.product(colours, numbers)]
        self.stack = self._rng.permutation(cards).tolist()
        # self.discarded = []

        # I've updated the numbers below
        rules_dict = dict([(2, 5), (3, 5), (4, 4), (5, 4)])
        nb_in_hand = rules_dict[self.nb_players]

        self.players = []

        for i in range(self.nb_players):
            player = Player(i)  # TODO: change to human readable
            self.players.append(player)
            self.deal_cards(player, nb_in_hand)

        to_play = self.round % self.nb_players
        self.current_player = self.players[to_play]

        self.num_connections = 1  # only initialised when there is one connection
        self.ready = False
        self.most_recent_move = None
        self.most_recent_pickup = None
        self.most_recent_move_life_lost = False

    def __str__(self):
        s = f"""
            Hanabi game with {self.nb_players} players at round {self.round}
             - Remaining lifes: {self.lifes}
             - Remaining clues: {self.clues}"""

        return textwrap.dedent(s)

    def check_endgame(self):
        if self.lifes == 0:
            print("YOU LOSE")
            self._finished = -1
            # exit()

        if self._endgame_count == 0:
            points = self.table.total_points()
            if points == 25:
                print("CONGRATULATIONS, YOU WON!")
            else:
                print(f'Total points: {points}')
            # exit()
            self._finished = points

        if len(self.stack) == 0 and self._endgame_count > 0:
            self._endgame_count -= 1

        return None

    def deal_cards(self, player, nb_cards):
        # In principle this function is not called if _endgame_flag is True
        for i in range(nb_cards):
            card = self.stack.pop()
            player.hand.append(card)
            player.hand_colour_info[card] = None
            player.hand_number_info[card] = None

            if len(self.stack) == 0:
                self._endgame_flag = True
                break

        if nb_cards == 1:  # This is the behaviour of pickup_card
            print("\nPicked up a {} {}".format(card.colour, card.number))
            self.most_recent_pickup = card

        return None

    def next_player(self):
        self.round += 1
        to_play = self.round % self.nb_players
        self.current_player = self.players[to_play]
        print("\nCurrent player is player {}".format(to_play))

        return None

    def player_played(self, action, **kwargs):
        assert action in ('play', 'discard', 'hint')
        # TOOD handle more gracefully than assert

        method = getattr(self.current_player, action)
        out = method(**kwargs)

        pass_hand = True

        if action == 'play':
            card = out
            play_succesful, stack_finished = self.table.play_card(card)
            self.most_recent_move_life_lost = False
            if self._endgame_flag is False:
                self.deal_cards(self.current_player, 1)

            if play_succesful is False:
                print("Life lost.")
                self.lifes -= 1
                self.most_recent_move_life_lost = True
                self.table.discard_card(card)

            if stack_finished and (self.clues<8):
                self.clues += 1

        elif action == 'discard':
            card = out
            self.table.discard_card(card)
            if self.clues<8:
                self.clues += 1
            self.most_recent_move_life_lost = False
            if self._endgame_flag is False:
                self.deal_cards(self.current_player, 1)

        elif action == 'hint':
            if self.clues < 1:
                print('No hints to left to give. Discard or play.')
                pass_hand = False
            else:
                to_player, info = out
                to_player.receive_hint(info)
                self.clues -= 1
                self.most_recent_move_life_lost = False

        self.check_endgame()

        return pass_hand

    def update_table(self, move):
        if (move[0] == 'play') or (move[0] == 'discard'):
            # format of move[1] should be an list with a single integer, indicating which card to play/discard
            card1 = self.current_player.hand[move[1][0]]
            next = self.player_played(
                move[0], card=card1)
            if next:
                self.next_player()
                self.most_recent_move = [move[0], card1]
        else:
            to_player = move[1][0]
            info = move[1][1]
            if info in ['red', 'blue', 'green', 'yellow', 'white']:
                next = self.player_played(
                    move[0], to_player=self.players[to_player], info=info)
            else:
                next = self.player_played(
                    move[0], to_player=self.players[to_player], info=int(info))

            if next:
                self.most_recent_move = move
                self.next_player()

        return None
