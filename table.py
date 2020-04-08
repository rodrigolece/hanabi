
import numpy as np


class Table(object):

    def __init__(self):
        self.red_stack = []
        self.blue_stack = []
        self.green_stack = []
        self.yellow_stack = []
        self.white_stack = []
        self.useful_discarded_stack = []
        self.useless_discarded_stack = []
        return None

    def total_points(self):
        total = 0

        for colour in ['red', 'blue', 'green', 'yellow', 'white']:
            stack_name = f'{colour}_stack'
            stack = getattr(self, stack_name)
            total += len(stack)

        return total

    def play_card(self, card):
        stack_name = f'{card.colour}_stack'
        stack = getattr(self, stack_name, None)
        play_succesful = False
        stack_finished = False

        if len(stack) > 0:  # the stack has cards
            top_card = stack[-1]
            if card.number == top_card.number + 1:
                stack.append(card)
                play_succesful = True
                if card.number == 5:
                    stack_finished = True
            # else not needed because play_succesful is False
        else:
            if card.number == 1:
                stack.append(card)
                play_succesful = True
            # same as above

        if play_succesful:
            for d in self.useful_discarded_stack:
                if d.colour == card.colour and d.number == card.number:
                    self.useful_discarded_stack.remove(d)
                    self.useless_discarded_stack.append(d)

        return play_succesful, stack_finished

    def discard_card(self, card):
        stack_name = f'{card.colour}_stack'
        stack = getattr(self, stack_name)

        if len(stack) == 0:
            self.useful_discarded_stack.append(card)
        elif stack[-1].number < card.number:
            self.useful_discarded_stack.append(card)
        else:
            self.useless_discarded_stack.append(card)

        return None
