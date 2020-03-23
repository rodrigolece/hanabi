
from tabulate import tabulate


class Player(object):
    def __init__(self, index):
        self.index = index  # player number
        self.hand = []  # how do we sort the hand?
        self.hand_colour_info = {}
        self.hand_number_info = {}
        return None

    def __str__(self):
        s = f'Player {self.index}:\n'
        tab = []
        for c in self.hand:
            tab.append([c.colour + ' ' + str(c.number),
                        str(self.hand_colour_info[c]).replace('None', '-')
                        + ' ' +
                        str(self.hand_number_info[c]).replace('None', '-')])
        s = s + tabulate(tab, headers=('hand', 'info'))
        return s

    def info_string(self):
        s = f'Player {self.index}:\n'
        tab = []
        for c in self.hand:
            tab.append([str(self.hand_colour_info[c]).replace('None', '-')
                        + ' ' +
                        str(self.hand_number_info[c]).replace('None', '-')])
        s = s + tabulate(tab, headers=('info known'))
        return s

    def decide_action(self, action, **kwargs):
        pass

    def move_card_in_hand(self, from_num, to_num):
        # This function will only sort if it is valid, and will not thrown an
        # error if invalid
        n = len(self.hand)
        if 0 <= from_num < n and 0 <= to_num < n:
            card = self.hand.pop(from_num)
            self.hand.insert(to_num, card)

        return None

    def play(self, card):
        # card = self.hand[card_num]
        print("\nPlaying a {} {}".format(card.colour, card.number))
        self.hand.remove(card)
        del self.hand_colour_info[card]
        del self.hand_number_info[card]

        return card

    def discard(self, card):
        # card = self.hand[card_num]
        print("\nDiscarding a {} {}".format(card.colour, card.number))
        self.hand.remove(card)
        del self.hand_colour_info[card]
        del self.hand_number_info[card]

        return card

    def hint(self, to_player, info):  # Not very elegant but it does the trick

        return to_player, info

    def receive_hint(self, info):  # independent of card
        if info in ['red', 'blue', 'green', 'yellow', 'white']:
            for card in self.hand:
                if card.colour == info:
                    self.hand_colour_info[card] = info
        else:
            for card in self.hand:
                if card.number == info:
                    self.hand_number_info[card] = info

        return None
