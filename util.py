
import pygame

from card import Card


__all__ = ['rgb',
           'Button', 'infoButton', 'game_buttons',
           'PygamePlayer', 'PygameTable']

rgb = {"red": (255, 0, 0),
       "green": (0, 255, 0),
       "blue": (0, 0, 255),
       "yellow": (255, 255, 0),
       "white": (255, 255, 255),
       "black": (0, 0, 0),
       "card": (142, 213, 200),
       "useless": (255, 176, 215),
       "background": (220, 220, 220)}


class Button:
    def __init__(self, text, x, y, width=150, height=100, color=rgb['black'], fs=40):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.rect = (x, y, width, height)
        self.fontsize = fs

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        font = pygame.font.SysFont("comicsans", self.fontsize)
        text = font.render(self.text, 1, rgb["white"])
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
                 width=150, height=100, color=rgb['black'], fs=40):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.rect = (x, y, width, height)
        self.fontsize = fs
        self.info = info

    def click(self, pos):
        x, y = pos
        clicked = None
        if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
            clicked = self.info
        return clicked


def wrap_text(text, font, width):
    """
    from : https://github.com/ColdrickSotK/yamlui/blob/master/yamlui/util.py#L82-L143
    Wrap text to fit inside a given width when rendered.
    :param text: The text to be wrapped.
    :param font: The font the text will be rendered in.
    :param width: The width to wrap to.
    """
    # text_lines = text.replace('\t', '    ').split('\n')
    text_lines = text.split('\n')

    if width is None or width == 0:
        return text_lines

    wrapped_lines = []
    for line in text_lines:
        line = line.rstrip() + ' '
        if line == ' ':
            wrapped_lines.append(line)
            continue

        # Get the leftmost space ignoring leading whitespace
        start = len(line) - len(line.lstrip())
        start = line.index(' ', start)
        while start + 1 < len(line):
            # Get the next potential splitting point
            next = line.index(' ', start + 1)
            if font.size(line[:next])[0] <= width:
                start = next
            else:
                wrapped_lines.append(line[:start])
                line = line[start + 1:]
                start = line.index(' ')
        line = line[:-1]
        if line:
            wrapped_lines.append(line)
    return wrapped_lines


def render_text_list(lines, font, colour=(255, 255, 255)):
    """
    from : https://github.com/ColdrickSotK/yamlui/blob/master/yamlui/util.py#L82-L143
    Draw multiline text to a single surface with a transparent background.
    Draw multiple lines of text in the given font onto a single surface
    with no background colour, and return the result.
    :param lines: The lines of text to render.
    :param font: The font to render in.
    :param colour: The colour to render the font in, default is white.
    """
    rendered = [font.render(line, True, colour).convert_alpha()
                for line in lines]

    line_height = font.get_linesize()
    width = max(line.get_width() for line in rendered)
    tops = [int(round(i * line_height)) for i in range(len(rendered))]
    height = tops[-1] + font.get_height()

    surface = pygame.Surface((width, height)).convert_alpha()
    # surface.fill((0, 0, 0, 0))
    surface.fill((128, 128, 128))
    for y, line in zip(tops, rendered):
        surface.blit(line, (0, y))

    return surface


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
    hint_players = [i for i in range(nb_players) if i!=player]
    btns_player = [Button(f'Player {i+1}', x_offset + x_space * i, y_offset)
                   for i in hint_players]

    btns_hint_clr = []
    btns_hint_nbr = []

    for i, clr in enumerate(['Red', 'Green', 'Yellow', 'White', 'Blue']):
        x = x_offset + x_space * i
        btn_clr = Button(clr, x, y_offset, color=rgb[clr.lower()], fs=25)
        btns_hint_clr.append(btn_clr)

        btn_nbr = Button(str(i + 1), x, y_offset + 100)
        btns_hint_nbr.append(btn_nbr)

    return btns_action, btns_card, btns_player, btns_hint_clr, btns_hint_nbr


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

    def draw(self, win, pos, fs=50, space=100):
        left, top = pos

        for i, card in enumerate(self.player.hand):
            top_card = top + space * i

            info_nbr = self.player.hand_number_info[card]
            s = info_nbr if info_nbr else '--'

            info_clr = self.player.hand_colour_info[card]
            c = info_clr if info_clr else 'black'

            if info_clr or info_nbr:
                hint_c = PygameCard(Card(c, s), hidden=False)
                hint_c.draw(win, (left + 60, top_card),
                            fs=fs, color=rgb['white'])

            pc = PygameCard(card, hidden=self._hidden)
            pc.draw(win, (left, top_card), fs=fs)

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
                                  win, rect, rgb['useless'], fs - 15)

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
