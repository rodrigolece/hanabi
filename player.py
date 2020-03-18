
class Player(object):
    def __init__(self, index):
        self.index = index
        self.hand = []  # how do we sort the hand?
        self.hand_colour_info = {}
        self.hand_number_info = {}
        # self.hand_info = {'numbers': [], 'colours': []}  # None for no info

        return None

    def __str__(self):
        s = f'\nPlayer {self.index}'
        for c in self.hand:
            s = s + f'\n {c.colour} {c.number}'
        return s

    def decide_action(self, action, **kwargs):
        pass

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
