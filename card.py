
class Card(object):
    def __init__(self, colour, number):
        self.colour = colour
        self.number = number

        return None

    def print_card(self):
        print("A {} {}".format(self.colour, self.number))
        return None
