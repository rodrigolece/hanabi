
import pickle
# import textwrap

from network import Network
from util import *

import pygame
pygame.font.init()

window_width = 1500
window_height = 1000
win = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Client")  # Give name of player?


def redrawWindow(win, game, p, stage_of_action, action, nb_players=4):
    # style

    win.fill(rgb['background'])

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
            nb_players=nb_players, player=p)

        # display player number
        your_player = f"You are Player {p+1}"
        font = pygame.font.SysFont("comicsans", 40)
        your_player_text = font.render(your_player, 1, rgb['black'])
        win.blit(your_player_text, (1050, 750))

        # print remaining lives and clues
        lives_remaining = f"Lives: {game.lifes}"
        clues_remaining = f"Clues: {game.clues}"
        font = pygame.font.SysFont("comicsans", 40)
        lives_remaining_text = font.render(lives_remaining, 1, rgb['black'])
        clues_remaining_text = font.render(clues_remaining, 1, rgb['black'])
        win.blit(lives_remaining_text, (1050, 800))
        win.blit(clues_remaining_text, (1050, 850))

        # print your own hand:
        pos = 50, 50  # Style here
        me = game.players[p]
        pc = PygamePlayer(me, hidden=True)
        pc.draw(win, pos)

        # print player hands
        i = 0  # enumerate doesn't work because of skip
        for player in game.players:
            if player.index == p:
                continue
            pc = PygamePlayer(player, hidden=False)
            pos = 200 + 150 * i, 50  # Style here
            pc.draw(win, pos)
            i += 1

        # print stacks
        pt = PygameTable(game.table)

        pos_stacks = 50, 590
        pos_useful = (800, 50)
        pos_useless = (800, 400)
        pt.draw(win, pos_stacks, pos_useful, pos_useless)

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
                f"Player {game.current_player.index+1}'s turn...", 1, rgb['white'])
            win.blit(text, (150, 750))

        # print most recent move
        if game.most_recent_move == None:
            prevMoveString = "Awaiting first move"
        elif (game.current_player.index - 1) % game.nb_players == p:
            prevMoveString = "You went last"
        else:

            if game.most_recent_move[0] == 'hint':
                prevMoveString = f"Player {((game.current_player.index-1)%game.nb_players)+1} gave a hint to player {game.most_recent_move[1][0] + 1} about cards which are {game.most_recent_move[1][1]}"
            elif game.most_recent_move[0] == 'play':
                prevMoveString = f"Player {((game.current_player.index-1)%game.nb_players)+1} played a {game.most_recent_move[1].colour} {game.most_recent_move[1].number} and picked up a {game.most_recent_pickup.colour} {game.most_recent_pickup.number} "
            elif game.most_recent_move[0] == 'discard':
                prevMoveString = f"Player {((game.current_player.index-1)%game.nb_players)+1} discarded a {game.most_recent_move[1].colour} {game.most_recent_move[1].number} and picked up a {game.most_recent_pickup.colour} {game.most_recent_pickup.number} "

        font = pygame.font.SysFont("comicsans", 30)
        prevMoveText = font.render(prevMoveString, 1, rgb['black'])
        win.blit(prevMoveText, (50, 550))

    pygame.display.update()


def main(net, player):
    print("in main loop")
    run = True
    clock = pygame.time.Clock()

    stage_of_action = 0
    move = ["none"]

    game = net.send_data("get")

    if game is None:
        print('Failed to fetch game')
        net.sock.close()
        exit()

    nb_players = game.nb_players

    btns_action, btns_card, btns_player, btns_hint_clr, btns_hint_nbr = game_buttons(
        nb_players=nb_players, player=player)

    while run:
        clock.tick(60)

        game = net.send_data("get")

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
                                    game = net.send_data(move)
                                    stage_of_action = 0
                                    move = ['none']

                    elif stage_of_action == 2:
                        for btn in btns_hint_clr:
                            if btn.click(pos):
                                move[1].append(btn.text.lower())
                                game = net.send_data(move)
                                stage_of_action = 0
                                move = ['none']
                        for btn in btns_hint_nbr:
                            if btn.click(pos):
                                move[1].append(int(btn.text))
                                game = net.send_data(move)
                                stage_of_action = 0
                                move = ["none"]


def redrawMenuWindow(menu_type, avail_games=None):

    win.fill(rgb['background'])
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
        # print("game not yet received")
        games = net.send_data(to_get)
        # print("games:",games)
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
                    # net.send(btn_info)
                    player = net.send_data(btn_info)
                    # player = 0
                    print("player received when joining:", player)
                    run = False

                elif btn_info.startswith('join'):
                    # reply = net.send(btn_info)
                    reply = net.send_data(btn_info)
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
