
import pygame


rgb = {"red": (255, 0, 0),
       "green": (0, 255, 0),
       "blue": (0, 0, 255),
       "yellow": (255, 255, 0),
       "white": (255, 255, 255)}


class Button:
    def __init__(self, text, x, y, width=150, height=100, color=(0, 0, 0), fs=40):
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
                 width=150, height=100, color=(0, 0, 0), fs=40):
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


def game_buttons(nb_players=4):
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
    btns_player = [Button(f'Player {i+1}', x_offset + x_space * i, y_offset)
                   for i in range(nb_players)]

    y_off = y_offset - 50
    btns_hint_clr = []
    btns_hint_nbr = []

    for i, clr in enumerate(['Red', 'Green', 'Yellow', 'White', 'Blue']):
        x = x_offset + x_space * i
        btn_clr = Button(clr, x, y_off - 50, color=rgb[clr.lower()], fs=25)
        btns_hint_clr.append(btn_clr)

        btn_nbr = Button(str(i + 1), x, y_offset + 50)
        btns_hint_nbr.append(btn_nbr)

    return btns_action, btns_card, btns_player, btns_hint_clr, btns_hint_nbr
