
class Card(object):
    def __init__(self, colour, number):
        self.colour = colour
        self.number = number

        return None

    def __str__(self):
        return "A {} {}".format(self.colour, self.number)
