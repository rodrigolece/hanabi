import pygame
from network import Network
import pickle
pygame.font.init()
import textwrap

width = 1000
height = 1000
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clrs = {"red":(255,0,0), "green": (0,255,0), "yellow":(255,255,0), "white":(255,255,255), "blue":(0,0,255)}

class Button:
    def __init__(self, text, x, y, width = 150, height = 100, color = (0,0,0)):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win, fontsize = 40):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", fontsize)
        text = font.render(self.text, 1, clrs["white"])
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

def wrap_text(text, font, width):

    """
    from : https://github.com/ColdrickSotK/yamlui/blob/master/yamlui/util.py#L82-L143
    Wrap text to fit inside a given width when rendered.
    :param text: The text to be wrapped.
    :param font: The font the text will be rendered in.
    :param width: The width to wrap to.
    """
    text_lines = text.replace('\t', '    ').split('\n')
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
                line = line[start+1:]
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
    surface.fill((0, 0, 0, 0))
    for y, line in zip(tops, rendered):
        surface.blit(line, (0, y))

    return surface

def redrawWindow(win, game, p, stage_of_action, action):
    win.fill((128,128,128))
    font = pygame.font.SysFont("comicsans", 16)

    # print player hands
    for i, player in enumerate(game.players):
        if player.index != p:
            s = player.__str__()
            text = wrap_text(s, font, 100)
            # text = font.render(textwrap.fill(s, 100), 1, (0, 255,255))
            win.blit(render_text_list(text, font, (0,0,0)), (80 + (i*100), 200))
        if player.index ==p:
            s = player.info_string()
            text = wrap_text(s, font, 100)
            # text = font.render(textwrap.fill(s, 100), 1, (0, 255,255))
            win.blit(render_text_list(text, font, (0,0,0)), (80 + (i*100), 200))

    # print discard piles
    s1, s2 = game.table.print_discard_piles()
    # print("s1", s1)
    text1 = wrap_text(s1, font, 100)
    win.blit(render_text_list(text1, font, (0,0,0)), (150, 400))
    text2 = wrap_text(s2, font, 100)
    win.blit(render_text_list(text2, font, (0,0,0)), (450, 400))


    # print current stack top cards in their colours

    font = pygame.font.SysFont("comicsans", 60)

    for i, key in enumerate(clrs.keys()):
        stack_name = f'{key}_stack'
        stack = getattr(game.table, stack_name)
        if len(stack)==0:
            text = font.render("--", 1, clrs[key])
        else:
            text = font.render(f"{stack[-1].number}", 1, clrs[key])
        win.blit(text, (100 + (i*100),650))

    #print play options
    if game.current_player.index == p:

        if (stage_of_action==0) and (action == "none"):
            for btn in btns1:
                btn.draw(win)
        elif (stage_of_action==1) and (action == 'hint'):
            for btn in btns3:
                btn.draw(win)

        elif (stage_of_action==1):
            for btn in btns2:
                btn.draw(win)

        elif stage_of_action==2:
            for btn in btns4:
                btn.draw(win, fontsize=25)
            for btn in btns5:
                btn.draw(win)

    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render(f"Player {game.current_player.index}'s turn...", 1, (255,0,0))
        win.blit(text, (150,750))

    pygame.display.update()


btns1 = [Button("Play", 50, 750, (0,0,0)), Button("Discard", 250, 750, (255,0,0)), Button("Hint", 450, 750, (0,255,0))]
btns2 = [Button("1", 50, 750, 50, 50, (0,0,0)),Button("2", 150, 750, 50, 50, (0,0,0)),Button("3", 250, 750, 50, 50, (0,0,0)),Button("4", 350, 750, 50, 50, (0,0,0)),Button("5", 450, 750, 50, 50, (0,0,0))] # for card to choose
btns3 = [Button("Player 1", 50, 750, 50, 50, (0,0,0)),Button("Player 2", 150, 750, 50, 50, (0,0,0)),Button("Player 3", 250, 750, 50, 50, (0,0,0)),Button("Player 4", 350, 750, 50, 50, (0,0,0))] # for palyer to giver hint to
btns4 = [Button("Red", 50, 700, 50, 50, clrs["red"]),Button("Green", 150, 700, 50, 50, clrs["green"]),Button("Yellow", 250, 700, 50, 50, clrs["yellow"]),Button("White", 350, 700, 50, 50, clrs["white"]),Button("Blue", 450, 700, 50, 50, clrs["blue"])]
btns5 = [Button("1", 50, 800, 50, 50, (0,0,0)),Button("2", 150, 800, 50, 50, (0,0,0)),Button("3", 250, 800, 50, 50, (0,0,0)),Button("4", 350, 800, 50, 50, (0,0,0)),Button("5", 450, 800, 50, 50, (0,0,0))] # for card to choose

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)
    stage_of_action = 0
    try:
        game = n.send("get")
        print("got the following game:", game)
    except:
        run = False
        print("Couldn't get game")
    while run:
        clock.tick(60)

        # try:
        #     game = n.send("get")
        #     # print("got the following game:", game)
        # except:
        #     run = False
        #     print("Couldn't get game")
        #     break

        redrawWindow(win, game, player, stage_of_action, "none")

        if game.current_player.index == player:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if stage_of_action ==0:
                        for btn in btns1:
                            if btn.click(pos):
                                    move = [btn.text.lower()]
                                    stage_of_action+=1
                                    redrawWindow(win, game, player, stage_of_action, move[0])
                    elif stage_of_action == 1:
                        if move[0] == "hint":
                            for btn in btns3:
                                if btn.click(pos):
                                        move.append([int(btn.text[-1])-1]) # minus one beacuse players and cards indexed from 0
                                        stage_of_action+=1
                                        redrawWindow(win, game, player, stage_of_action, move[0])

                        else:
                            for btn in btns2:
                                if btn.click(pos):
                                        move.append([int(btn.text)-1])
                                        game = n.send(move)
                                        # n.send(move)
                                        stage_of_action=0
                                        redrawWindow(win, game, player, stage_of_action, move[0])

                    elif stage_of_action == 2:
                        for btn in btns4:
                            if btn.click(pos):
                                    move[1].append(btn.text.lower())
                                    game = n.send(move)
                                    stage_of_action=0
                                    redrawWindow(win, game, player, stage_of_action, move[0])
                        for btn in btns5:
                            if btn.click(pos):
                                    move[1].append(int(btn.text))
                                    game = n.send(move)
                                    stage_of_action=0
                                    # for i in game.players:
                                    #     print(i)
                                    redrawWindow(win, game, player, stage_of_action, move[0])

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255,0,0))
        win.blit(text, (100,200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()
