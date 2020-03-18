

class Table(object):

    def __init__(self):
        self.red_stack = []
        self.blue_stack = []
        self.green_stack = []
        self.yellow_stack = []
        self.white_stack = []
        self.discarded_stack = []
        return None

    def play_card(self, card):
        stack_name = f'{card.colour}_stack'
        stack = getattr(self, stack_name, None)
        play_succesful = False

        if len(stack) > 0:  # the stack has cards
            top_card = stack[-1]
            if card.number == top_card.number + 1:
                stack.append(card)
                play_succesful = True
            # else not needed because play_succesful is False
        else:
            if card.number == 1:
                stack.append(card)
                play_succesful = True
            # same as above

        return play_succesful
