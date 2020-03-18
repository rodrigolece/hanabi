

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
            useful_stack_card_info = [(c.colour, c.number) for c in self.useful_discarded_stack]
            stack_indices = [i for i, x in enumerate(useful_stack_card_info) if x == (card.colour, card.number)]
            if len(stack_indices)>0:
                for i in stack_indices:
                    self.useless_discarded_stack.append(self.useful_discarded_stack.pop(i))

        return play_succesful

    def discard_card(self, card):
        stack_name = f'{card.colour}_stack'
        stack = getattr(self, stack_name, None)
        if len(stack)==0:
            self.useful_discarded_stack.append(card)
        elif stack[-1].number<card.number:
            self.useful_discarded_stack.append(card)
        else:
            self.useless_discarded_stack.append(card)

        return None

    def print_discard_piles(self):
        print("\nUseful discard pile:")
        for card in self.useful_discarded_stack:
            print(f'\n {card.colour} {card.number}')
        print("\nUseless discard pile:")
        for card in self.useless_discarded_stack:
            print(f'\n {card.colour} {card.number}')

        return None

    def print_stacks(self):
        print("Current stacks:")
        for i in ['red', 'blue', 'green', 'yellow', 'white']:
            s = f"{i} stack:"
            stack_name = f'{i}_stack'
            stack = getattr(self, stack_name, None)
            for c in stack:
                s = s + f" {c.number}"
            print(s)


        return None
