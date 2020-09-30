"""Card class"""


class Card(object):
    def __init__(self, colour, number, id):
        self.colour = colour
        self.number = number
        self._id = id

        return None

    def __str__(self):
        return f'Card: {self.colour}-{self.number}'

    def serialise(self):
        return {'id': self._id, 'colour': self.colour, 'number': self.number}
