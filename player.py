
class Player(object):
    def __init__(self, index):
        self.index = index
        self.hand = []  # how do we sort the hand?
        self.hand_colour_info = {}
        self.hand_number_info = {}
        # self.hand_info = {'numbers': [], 'colours': []}  # None for no info

        return None

    def play(self, card_num):
        card = self.hand[card_num]
        print("\nPlaying a {} {}".format(card.colour, card.number))
        self.hand.remove(card)
        del self.hand_colour_info[card]
        del self.hand_number_info[card]

        return card

    def discard(self, card_num):
        card = self.hand[card_num]
        print("\nDiscarding a {} {}".format(card.colour, card.number))
        self.hand.remove(card)
        del self.hand_colour_info[card]
        del self.hand_number_info[card]

        return card

    def hint(self, other_player, info):
        # clues should go down
        pass
