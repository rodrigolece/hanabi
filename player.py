
class Player(object):
    def __init__(self, index):
        self.index = index
        self.hand = []  # how do we sort the hand?
        self.hand_info = {}  # dict from card to info (colour and or number)

        return None

    def info(self, other_player, info):
        # clues should go down
        pass

    def discard(card):
        # clues should go up
        pass

    def play(card):
        pass
