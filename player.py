
class Player(object):
    def __init__(self, index):
        self.index = index
        self.hand = []  # how do we sort the hand?
        self.hand_info = {'numbers':[], 'colours':[]}  # None for no info
        return None

    def info(self, other_player, info):
        # clues should go down
        pass

    def play(self, card_num):
        print("\nPlaying a {} {}".format(self.hand[card_num].colour, self.hand[card_num].number))
        card = self.hand.pop(card_num)
        self.hand_info["numbers"].pop(card_num)
        self.hand_info["colours"].pop(card_num)
        return card

    def discard(self, card_num):
        print("\nDiscarding a {} {}".format(self.hand[card_num].colour, self.hand[card_num].number))
        card = self.hand.pop(card_num)
        self.hand_info["numbers"].pop(card_num)
        self.hand_info["colours"].pop(card_num)
        return card

    def pickup(self, card):
        print("\nPicked up a {} {}".format(card.colour, card.number))
        self.hand.append(card)

        return None
