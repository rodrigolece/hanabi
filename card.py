"""Card class"""


class Card(object):
    def __init__(self, colour, number):
        self.colour = colour
        self.number = number

        return None

    def __str__(self):
        return f'Card: {self.colour}-{self.number}'

    def serialise(self):
        return {'colour': self.colour, 'number': self.number}
