
import numpy as np
from tabulate import tabulate


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

        if play_succesful:
            useful_stack_card_info = [(c.colour, c.number)
                                      for c in self.useful_discarded_stack]
            stack_indices = [i for i, x in enumerate(
                useful_stack_card_info) if x == (card.colour, card.number)]
            if len(stack_indices) > 0:
                for i in stack_indices:
                    self.useless_discarded_stack.append(
                        self.useful_discarded_stack.pop(i))

        return play_succesful

    def discard_card(self, card):
        stack_name = f'{card.colour}_stack'
        stack = getattr(self, stack_name, None)
        if len(stack) == 0:
            self.useful_discarded_stack.append(card)
        elif stack[-1].number < card.number:
            self.useful_discarded_stack.append(card)
        else:
            self.useless_discarded_stack.append(card)

        return None

    def print_discard_piles(self):
        useful = np.zeros((5, 5), dtype=str).tolist()
        useless = np.zeros((5, 5), dtype=str).tolist()

        colours = ['red', 'blue', 'green', 'yellow', 'white']
        map = dict(zip(colours, range(5)))

        for card in self.useful_discarded_stack:
            col = map[card.colour]
            row = card.number - 1
            s = str(card.number)
            if useful[row][col]:  # if the entry is not empty, prepend comma
                s = ',' + s
            useful[row][col] += s

        for card in self.useless_discarded_stack:
            col = map[card.colour]
            row = card.number - 1
            s = str(card.number)
            if useless[row][col]:
                s = ',' + s
            useless[row][col] += s

        # Not elegant, but I insert zeros to replace below
        for i in range(5):
            for j in range(5):
                useful[i][j] = '0' if not useful[i][j] else useful[i][j]
                useless[i][j] = '0' if not useless[i][j] else useless[i][j]

        print("\nUseful discard pile:\n")
        print(tabulate(useful, headers=colours).replace('0', '.'))

        print("\nUseless discard pile:")
        print(tabulate(useless, headers=colours).replace('0', '.'))

        return None

    def print_stacks(self):
        mat = np.zeros((5, 5), dtype=int)
        colours = ['red', 'blue', 'green', 'yellow', 'white']

        for i, c in enumerate(colours):
            stack_name = f'{c}_stack'
            stack = getattr(self, stack_name)
            if len(stack) > 0:
                top_card = stack[-1]
                n = top_card.number
                mat[:n, i] = range(1, n + 1)

        tab = tabulate(mat, headers=colours).replace('0', '.')

        print("\nCurrent stacks:\n")
        print(tab)

        return None
