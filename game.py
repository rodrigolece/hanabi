"""Main class that models the game."""
import itertools
import textwrap
import json
import numpy as np

from player import Player
from card import Card
from table import Table


class Hanabi(object):

    def __init__(self, nb_players, id_game=0, seed=42, verbose=False):
        # Below is used in online games
        self._num_connections = 1  # a game is initialised when there is 1 connection
        self._ready = False
        self._finished = None  # used for number of points at the end
        self._id_game = id_game

        self.verbose = verbose
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

        rules_dict = dict([(2, 5), (3, 5), (4, 4), (5, 4)])
        nb_in_hand = rules_dict[self.nb_players]

        self.players = []

        for i in range(self.nb_players):
            player = Player(i)  # TODO: change to human readable
            self.players.append(player)
            self.deal_cards(player, nb_in_hand)

        to_play = self.round % self.nb_players
        self.current_player = self.players[to_play]

        # This is used in displayed game
        self.num_connections = 1  # TODO: not used? _num_connections above is used?
        self.ready = False
        self.most_recent_move = None
        self.most_recent_pickup = None
        self.most_recent_move_life_lost = False

    def __str__(self):
        s = f"""
            Hanabi game with {self.nb_players} players at round {self.round}
             - Remaining lifes: {self.lifes}
             - Remaining clues: {self.clues}
             - Remaining cards in stack: {len(self.stack)}"""

        return textwrap.dedent(s)

    def serialise(self):
        out = dict()
        out['game'] = {'round': self.round,
                       'current_id': self.current_player.index,
                       'clues': self.clues,
                       'lifes': self.lifes,
                       'endgame': self._endgame_flag,
                       'finished': self._finished
                       }
        out['players'] = [p.serialise() for p in self.players]
        out['stacks'] = self.table.serialise()

        return out  # json.dumps(out)

    def check_endgame(self):
        if self.lifes == 0:
            if self.verbose:
                print('YOU LOSE')
            self._finished = -1
            # exit()

        if self._endgame_count == 0:
            points = self.table.total_points()
            self._finished = points
            end_message = 'CONGRATULATIONS, YOU WON!' if points == 25 else f'Total points: {points}'
            # exit()
            if self.verbose:
                print(end_message)

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
            self.most_recent_pickup = card
            if self.verbose:
                print("\nPicked up a {} {}".format(card.colour, card.number))

        return None

    def next_player(self):
        self.round += 1
        to_play = self.round % self.nb_players
        self.current_player = self.players[to_play]
        if self.verbose:
            print("\nCurrent player is player {}".format(to_play))

        return None

    def player_played(self, action, **kwargs):
        assert action in ('play', 'discard', 'hint')
        # TODO: handle more gracefully than assert

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
                self.lifes -= 1
                self.most_recent_move_life_lost = True
                self.table.discard_card(card)
                if self.verbose:
                    print("Life lost.")

            if stack_finished and (self.clues < 8):
                self.clues += 1

        elif action == 'discard':
            card = out
            self.table.discard_card(card)
            if self.clues < 8:
                self.clues += 1
            self.most_recent_move_life_lost = False
            if self._endgame_flag is False:
                self.deal_cards(self.current_player, 1)

        elif action == 'hint':
            if self.clues < 1:
                # print('No hints to left to give. Discard or play.')
                pass_hand = False
            else:
                to_player, info = out
                to_player.receive_hint(info)
                self.clues -= 1
                self.most_recent_move_life_lost = False

        self.check_endgame()

        return pass_hand

    def update_table(self, action, card_id=None, player_id=None, info=None):
        """Translate card or player index and execute turn."""
        if action in ['play', 'discard']:
            assert card_id is not None  # TODO: handle more gracefully

            card = self.current_player.hand[card_id]
            pass_hand = self.player_played(action, card=card)

        else:  # hint
            assert player_id is not None
            assert info is not None  # TODO: handle more gracefully

            to_player = self.players[player_id]
            if info in ['red', 'blue', 'green', 'yellow', 'white']:
                pass
            elif info in [str(i) for i in range(1, 6)]:
                info = int(info)
            else:
                raise ValueError

            pass_hand = self.player_played(action,
                                           to_player=to_player,
                                           info=info)

        if pass_hand:
            self.next_player()
            self.most_recent_move = [action, card_id, player_id, info]
        # TODO: else, repeat play attempt

        return None
