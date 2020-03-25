
import pickle
# import textwrap

from network import Network
from util import Button, infoButton, wrap_text, render_text_list, game_buttons

import pygame
pygame.font.init()

window_width = 1000
window_height = 1000
win = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Client")  # Give name of player?

rgb = {"red": (255, 0, 0),
       "green": (0, 255, 0),
       "blue": (0, 0, 255),
       "yellow": (255, 255, 0),
       "white": (255, 255, 255)}


def redrawWindow(win, game, p, stage_of_action, action, nb_players=4):
    # style
    player_width = 200
    current_player_width = 100

    win.fill((128, 128, 128))

    if game._ready is False:
        font = pygame.font.SysFont("comicsans", 60)
        diff = game.nb_players - game._num_connections
        other_s = 'other' if diff == 1 else 'others'
        text = font.render(
            f"Waiting for {diff} {other_s} to join ...", 1, rgb['white'])
        win.blit(text, (100, 300))

    else:
        font = pygame.font.SysFont("comicsans", 16)
        btns_action, btns_card, btns_player, btns_hint_clr, btns_hint_nbr = game_buttons(
            nb_players=nb_players)

        # print player hands
        for i, player in enumerate(game.players):
            if player.index != p:
                s = player.__str__()
                text = wrap_text(s, font, player_width)
                # text = font.render(textwrap.fill(s, 100), 1, (0, 255,255))
                win.blit(render_text_list(text, font),
                         (80 + (i * 100), 200))
            if player.index == p:
                s = player.info_string()
                text = wrap_text(s, font, current_player_width)
                # text = font.render(textwrap.fill(s, 100), 1, (0, 255,255))
                win.blit(render_text_list(text, font),
                         (80 + (i * 100), 200))

        # print discard piles
        s1, s2 = game.table.print_discard_piles()
        # print("s1", s1)
        text1 = wrap_text(s1, font, 400)
        win.blit(render_text_list(text1, font), (150, 400))  # (0, 0, 0)
        text2 = wrap_text(s2, font, 400)
        win.blit(render_text_list(text2, font), (450, 400))  # (0, 0, 0)

        # print current stack top cards in their colours
        font = pygame.font.SysFont("comicsans", 60)

        for i, key in enumerate(['red', 'blue', 'green', 'yellow', 'white']):
            stack_name = f'{key}_stack'
            stack = getattr(game.table, stack_name)
            if len(stack) == 0:
                text = font.render("--", 1, rgb[key])
            else:
                text = font.render(f"{stack[-1].number}", 1, rgb[key])
            win.blit(text, (100 + (i * 100), 650))

        # print play options
        if game.current_player.index == p:

            if (stage_of_action == 0) and (action == "none"):
                for btn in btns_action:
                    btn.draw(win)

            elif (stage_of_action == 1) and (action == "hint"):
                for btn in btns_player:
                    btn.draw(win)

            elif (stage_of_action == 1):
                for btn in btns_card:
                    btn.draw(win)

            elif stage_of_action == 2:
                for btn in btns_hint_clr:
                    btn.draw(win)  # fontsize=25
                for btn in btns_hint_nbr:
                    btn.draw(win)

        else:
            font = pygame.font.SysFont("comicsans", 60)
            text = font.render(
                f"Player {game.current_player.index}'s turn...", 1, rgb['white'])
            win.blit(text, (150, 750))

    pygame.display.update()


def main(net, player):
    run = True
    clock = pygame.time.Clock()

    stage_of_action = 0
    move = ["none"]

    game = net.send("get")

    if game is None:
        print('Failed to fetch game')
        net.sock.close()
        exit()

    nb_players = game.nb_players

    btns_action, btns_card, btns_player, btns_hint_clr, btns_hint_nbr = game_buttons(
        nb_players=nb_players)

    while run:
        clock.tick(60)

        game = net.send("get")

        redrawWindow(win, game, player, stage_of_action,
                     move[0], nb_players=nb_players)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if game.current_player.index == player:

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if stage_of_action == 0:
                        for btn in btns_action:
                            if btn.click(pos):
                                move = [btn.text.lower()]
                                stage_of_action += 1

                    elif stage_of_action == 1:
                        if move[0] == "hint":
                            for btn in btns_player:
                                if btn.click(pos):
                                    # minus one beacuse players and cards indexed from 0
                                    move.append([int(btn.text[-1]) - 1])
                                    stage_of_action += 1
                        else:
                            for btn in btns_card:
                                if btn.click(pos):
                                    move.append([int(btn.text) - 1])
                                    game = net.send(move)
                                    stage_of_action = 0
                                    move = ['none']

                    elif stage_of_action == 2:
                        for btn in btns_hint_clr:
                            if btn.click(pos):
                                move[1].append(btn.text.lower())
                                game = net.send(move)
                                stage_of_action = 0
                                move = ['none']
                        for btn in btns_hint_nbr:
                            if btn.click(pos):
                                move[1].append(int(btn.text))
                                game = net.send(move)
                                stage_of_action = 0
                                move = ["none"]


def redrawMenuWindow(menu_type, avail_games=None):

    win.fill((128, 128, 128))
    if menu_type == 'main':
        btn_start = infoButton('START NEW GAME', 300, 450,
                               'start-game', width=400, fs=30)
        btns = [btn_start]
        for i, game_id in enumerate(avail_games.keys()):
            btn_join = infoButton(f'JOIN GAME {game_id}: {avail_games[game_id].nb_players} player', 50 + 400 * i, 600,
                                  f'join-{game_id}', width=400, fs=30)
            btns.append(btn_join)

    elif menu_type == 'start-game':
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Select number of players:", 1, rgb['white'])
        win.blit(text, (100, 300))

        btns = [infoButton(str(n), 50 + 200 * i, 450, f'start-{n}')
                for i, n in enumerate(range(2, 6))]

    # elif menu_type == 'join-game':
    #     font = pygame.font.SysFont("comicsans", 60)
    #     text = font.render("Select number of players:", 1, rgb['white'])
    #     win.blit(text, (100, 300))
    #
    #     btns = [infoButton(str(n), 50 + 200 * i, 450, f'join-{n}')
    #             for i, n in enumerate(range(4))]

    # elif menu_type == 'waiting':
    #     btns = []  # no buttons in this screen
    #
    #     font = pygame.font.SysFont("comicsans", 60)
    #     text = font.render("Waiting for others to join ...", 1, rgb['white'])
    #     win.blit(text, (100, 300))

    for btn in btns:
        btn.draw(win)

    pygame.display.update()

    return btns


def menu_screen():
    run = True
    clock = pygame.time.Clock()
    net = Network()

    menu_type = 'main'
    to_get = 'get_avail_games'

    while run:
        clock.tick(60)

        games = net.send(to_get)

        btns = redrawMenuWindow(menu_type, games)
        btn_info = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                for btn in btns:
                    if btn.click(pos):
                        btn_info = btn.click(pos)

                if btn_info == 'start-game':
                    menu_type = btn_info

                elif btn_info.startswith('start'):
                    net.send(btn_info)
                    player = 0
                    print("player received when joining:", player)
                    run = False

                elif btn_info.startswith('join'):
                    reply = net.send(btn_info)
                    if isinstance(reply, int):
                        player = reply
                        print("player received when joining:", player)
                        run = False
                    elif reply == 'choose_again':
                        print('Game is full, choose again')
                        menu_type = 'main'

    # pass control to main
    main(net, int(player))


# This is where the client is started (at the menu screen)
menu_screen()
