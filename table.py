

class Table(object):

    def __init__(self):
        self.red_stack = []
        self.blue_stack = []
        self.green_stack = []
        self.yellow_stack = []
        self.white_stack = []

        return None

    def play_card(self, card):
        stack_name = f'{card.colour}_stack'
        stack = getattr(self, stack_name, None)

        if len(stack) > 0:  # the stack has cards
            top_card = stack[-1]
            if card.number == top_card.number + 1:
                stack.append(card)
            else:
                print("card discarded")
                # TODO discard card
                # TODO lifes should decrease
        else:
            if card.number == 0:
                stack.append(card)
            else:
                print("card discarded")
                # TODO discard card
                # TODO lifes should decrease
