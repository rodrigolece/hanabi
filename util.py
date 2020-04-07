
import pygame

from card import Card


__all__ = ['rgb',
           'Button', 'infoButton', 'game_buttons', 'pos_from_center',
           'PygamePlayer', 'PygameTable']

rgb = {"red": (255, 0, 0),
       "green": (0, 255, 0),
       "blue": (0, 0, 255),
       "yellow": (255, 255, 0),
       "white": (255, 255, 255),
       "black": (0, 0, 0),
       "card": (142, 213, 200),
       "darkgrey": (135, 135, 135),
       "background": (220, 220, 220)}


class Button:
    def __init__(self, text, x, y, width=150, height=100, color=rgb['black'], fs=40, text_colour="white"):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.rect = (x, y, width, height)
        self.fontsize = fs
        self.text_colour = text_colour

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        font = pygame.font.SysFont("comicsans", self.fontsize)
        text = font.render(self.text, 1, rgb[self.text_colour])
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x, y = pos
        clicked = False
        if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
            clicked = True
        return clicked


class infoButton(Button):
    def __init__(self, text, x, y, info,
                 width=150, height=100, color=rgb['black'], fs=40, text_colour="white"):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.rect = (x, y, width, height)
        self.fontsize = fs
        self.info = info
        self.text_colour = text_colour

    def click(self, pos):
        x, y = pos
        clicked = None
        if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
            clicked = self.info
        return clicked


def pos_from_center(x_center, y_center, width, height):
    x = x_center - (width / 2)
    y = y_center - (height / 2)
    return x, y


def game_buttons(nb_players=4, player=0):
    rules_dict = dict([(2, 5), (3, 5), (4, 4), (5, 4)])
    nb_in_hand = rules_dict[nb_players]

    # Defaults
    x_offset = 50
    x_space = 200
    y_offset = 750

    btns_action = [Button("Play", 50, y_offset),
                   Button("Discard", 250, y_offset, color=rgb['red']),
                   Button("Hint", 450, y_offset, color=rgb['green'])]

    # for card to choose
    btns_card = [Button(str(i + 1), x_offset + x_space * i, y_offset)
                 for i in range(nb_in_hand)]

    # for player to give hint to
    hint_players = [i for i in range(nb_players) if i != player]
    btns_player = [Button(f'Player {i+1}', x_offset + x_space * i, y_offset)
                   for i in hint_players]

    # go back button

    btns_go_back = [infoButton("Go back", 570, 590, info="back_to_stage_0"), infoButton(
        "Go back", 570, 590, info="back_to_stage_0")]

    btns_hint_clr = []
    btns_hint_nbr = []

    for i, clr in enumerate(['Red', 'Green', 'Yellow', 'White', 'Blue']):
        x = x_offset + x_space * i
        btn_clr = Button(clr, x, y_offset,
                         color=rgb[clr.lower()], fs=25, text_colour="black")
        btns_hint_clr.append(btn_clr)

        btn_nbr = Button(str(i + 1), x, y_offset + 100)
        btns_hint_nbr.append(btn_nbr)

    return btns_action, btns_card, btns_player, btns_hint_clr, btns_hint_nbr, btns_go_back


class PygameCard(object):

    def __init__(self, card, hidden=False, show_clr=True, show_nbr=True):
        self.card = card
        self._hidden = hidden
        return None

    def draw(self, win, pos, width=50, height=70, color=rgb['card'], fs=50):
        rect = *pos, width, height
        pygame.draw.rect(win, color, rect)

        if not self._hidden:
            font = pygame.font.SysFont('comicsans', fs)
            s, c = f'{self.card.number}', self.card.colour
            text = font.render(s, 1, rgb[c])  # 1 is antialias, what is that?
            x, y = pos
            x += (width - text.get_width()) // 2
            y += (height - text.get_height()) // 2
            win.blit(text, (x, y))  # area=None, special_flags=0
            return None


class PygamePlayer(object):

    def __init__(self, player, hidden=False):
        self.player = player
        self._hidden = hidden

        return None

    def draw(self, win, pos, fs=50, space=140):
        left, top = pos

        font = pygame.font.SysFont("comicsans", 20)
        text = font.render(f"Player {self.player.index + 1}", 1, (0, 0, 0))
        win.blit(text, (left, top - 18))

        for i, card in enumerate(self.player.hand):
            # top_card = top + space * i
            left_card = left + space * i

            info_nbr = self.player.hand_number_info[card]
            s = info_nbr if info_nbr else '--'

            info_clr = self.player.hand_colour_info[card]
            c = info_clr if info_clr else 'black'

            if info_clr or info_nbr:
                hint_c = PygameCard(Card(c, s), hidden=False)
                # hint_c.draw(win, (left + 60, top_card),
                #             fs=fs, color=rgb['white'])
                hint_c.draw(win, (left_card + 60, top),
                            fs=fs, color=rgb["darkgrey"])

            pc = PygameCard(card, hidden=self._hidden)
            # pc.draw(win, (left, top_card), fs=fs)
            pc.draw(win, (left_card, top), fs=fs)

        return None


class PygameTable():
    def __init__(self, table):
        self.table = table
        return None

    def draw(self, win, pos_stacks, pos_useful, pos_useless, fs=50):
        colours = ['red', 'blue', 'green', 'yellow', 'white']
        map = dict(zip(colours, range(5)))

        # The main playing stacks
        left, top = pos_stacks
        rect = left, top, 490, 110  # Style here
        pygame.draw.rect(win, rgb['white'], rect)

        for i, clr in enumerate(colours):
            stack_name = f'{clr}_stack'
            stack = getattr(self.table, stack_name)

            pos = left + 20 + i * 100, top + 20
            if len(stack) == 0:
                card = PygameCard([], hidden=True)
                card.draw(win, pos, color=rgb['white'])
            else:
                card = PygameCard(stack[-1], hidden=False)
                card.draw(win, pos, fs=fs)

        # The useful discarded
        rect = *pos_useful, 500, 300  # Style here
        self._print_discard_stack(self.table.useful_discarded_stack,
                                  win, rect, rgb['white'], fs - 15)

        # The useless_discarded_stack
        rect = *pos_useless, 500, 300  # Style here
        self._print_discard_stack(self.table.useless_discarded_stack,
                                  win, rect, rgb["darkgrey"], fs - 15)

    def _print_discard_stack(self, stack, win, rect, clr, fs):
        left, top, width, height = rect
        pygame.draw.rect(win, clr, rect)

        # area to put the cards
        height -= 40
        width -= 40

        top += 20
        left += 20

        # We calculate available space based on height
        card_space_y = height // 5
        card_height = card_space_y * 4 // 5  # 80 percent should be the card
        card_width = card_height * 5 // 7

        card_space_x = width // 5

        colours = ['red', 'blue', 'green', 'yellow', 'white']
        map = dict(zip(colours, range(5)))

        previously_drawn = []
        for card in stack:
            pc = PygameCard(card, hidden=False)
            i = card.number - 1
            j = map[card.colour]
            count = previously_drawn.count((i, j))
            previously_drawn.append((i, j))
            pos = left + card_space_x * j + 20 * count, top + card_space_y * i
            pc.draw(win, pos, width=card_width, height=card_height, fs=fs)
