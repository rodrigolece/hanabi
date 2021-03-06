
import pickle

from network import Network
from util import *

import pygame
from pygame.locals import *
pygame.init()
# pygame.font.init()


class Client(object):
    def __init__(self, ip_addr, port, window_width=1500, window_height=1000):
        self.ip_addr = ip_addr
        self.port = port

        self.window_width = window_width
        self.window_height = window_height
        self.real_win = pygame.display.set_mode((window_width, window_height),
                                                HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.win = pygame.surface.Surface((window_width, window_height))
        self.resized_size = (window_width, window_height)
        self.resized_flag = False
        pygame.display.set_caption("Hanabi")

        self.menu_screen()  # the client is started at the menu screen

    def blit_resized_win(self):
        # self.real_win = pygame.display.set_mode(self.resized_size,
        #                                         HWSURFACE | DOUBLEBUF | RESIZABLE)
        scaled_win = pygame.transform.scale(self.win, self.resized_size)
        self.real_win.blit(scaled_win, (0, 0))

        self.resized_flag = False

        return None

    def scale_pos(self, real_win_pos):
        x = real_win_pos[0] * self.window_width // self.resized_size[0]
        y = real_win_pos[1] * self.window_height // self.resized_size[1]
        # print('real:', real_win_pos)
        # print('scaled:', (x, y), '\n')

        return (x, y)

    def gameWindow(self, game, p, stage_of_action, action, nb_players=4, game_ended=False):
        win = self.win
        font = pygame.font.SysFont("comicsans", 16)
        btns_action, btns_card, btns_player, btns_hint_clr, btns_hint_nbr, btns_go_back = game_buttons(
            nb_players=nb_players, player=p)

        # display player number
        your_player = f"You are Player {p+1}"
        font = pygame.font.SysFont("comicsans", 40)
        your_player_text = font.render(your_player, 1, rgb['black'])
        win.blit(your_player_text, (1050, 750))

        # print remaining lives and clues nad cards in deck
        lives_remaining = f"Lives: {game.lifes}"
        clues_remaining = f"Clues: {game.clues}"
        cards_in_deck_remaining = f"Cards left in deck: {len(game.stack)}"
        font = pygame.font.SysFont("comicsans", 40)
        lives_remaining_text = font.render(lives_remaining, 1, rgb['black'])
        clues_remaining_text = font.render(clues_remaining, 1, rgb['black'])
        cards_in_deck_remaining_text = font.render(
            cards_in_deck_remaining, 1, rgb['black'])
        win.blit(lives_remaining_text, (1050, 800))
        win.blit(clues_remaining_text, (1050, 850))
        win.blit(cards_in_deck_remaining_text, (1050, 900))

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
            # pos = 200 + 150 * i, 50  # Style here
            pos = 50, 50 + 100 * (1 + i)  # Style here
            pc.draw(win, pos)
            i += 1

        # print stacks
        pt = PygameTable(game.table)

        pos_stacks = 50, 590
        pos_useful = (800, 50)
        pos_useless = (800, 400)
        pt.draw(win, pos_stacks, pos_useful, pos_useless)

        # print play options
        if game.current_player.index == p and game_ended is False:

            if (stage_of_action == 0) and (action == "none"):
                if game.clues > 0:
                    for btn in btns_action:
                        btn.draw(win)
                else:
                    for btn in btns_action:
                        if btn.text != "Hint":
                            btn.draw(win)

            elif (stage_of_action == 1) and (action == "hint"):
                for btn in btns_player:
                    btn.draw(win)
                btns_go_back[0].draw(win)

            elif (stage_of_action == 1):
                for btn in btns_card:
                    btn.draw(win)
                btns_go_back[0].draw(win)

            elif stage_of_action == 2:
                for btn in btns_hint_clr:
                    btn.draw(win)  # fontsize=25
                for btn in btns_hint_nbr:
                    btn.draw(win)
                btns_go_back[1].draw(win)

        elif game_ended is False:
            font = pygame.font.SysFont("comicsans", 60)
            text = font.render(
                f"Player {game.current_player.index+1}'s turn...", 1, rgb['black'])
            win.blit(text, (50, 750))

        # print most recent move
        if game.most_recent_move == None:
            prevMoveString = "Awaiting first move"
        elif (game.current_player.index - 1) % game.nb_players == p:
            if game.most_recent_move[0] == 'hint':
                prevMoveString = f"You gave a hint to player {game.most_recent_move[1][0] + 1} about cards which are {game.most_recent_move[1][1]}"
            elif game.most_recent_move[0] == 'play':
                prevMoveString = f"You played a {game.most_recent_move[1].colour} {game.most_recent_move[1].number}"
            elif game.most_recent_move[0] == 'discard':
                prevMoveString = f"You discarded a {game.most_recent_move[1].colour} {game.most_recent_move[1].number}"
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

        # print lost life message:
        if game.most_recent_move_life_lost:
            font = pygame.font.SysFont("comicsans", 40)
            s = "You lost a life!"
            text = font.render(s, 1, rgb['red'])
            win.blit(text, (1200, 800))

    def redrawWindow(self, game, p, stage_of_action, action, nb_players=4):
        win = self.win
        window_width, window_height = self.window_width, self.window_height

        win.fill(rgb['background'])

        if game._ready is False:
            font = pygame.font.SysFont("comicsans", 60)
            diff = game.nb_players - game._num_connections
            other_s = 'other' if diff == 1 else 'others'
            s = f"Waiting for {diff} {other_s} to join ..."
            s_width, s_height = font.size(s)
            posx, posy = pos_from_center(
                window_width / 2, window_height / 4, s_width, s_height)
            text = font.render(s, 1, rgb['black'])
            win.blit(text, (posx, posy))

        elif game._finished:
            self.gameWindow(game, p, stage_of_action,
                            action, nb_players=nb_players, game_ended=True)

            font = pygame.font.SysFont("comicsans", 60)
            points = game._finished
            if points < 0:
                s = 'YOU LOSE'
            else:
                if points == 25:
                    s = 'YOU WON!'
                else:
                    s = f'Game ended with total points: {points}'
            # s += '\n\nClick to play again'
            s_width, s_height = font.size(s)
            text = font.render(s, 1, rgb['red'])
            posx, posy = 50, 750  # + text.get_width(), 750 + text.get_height()
            win.blit(text, (posx, posy))

        else:
            self.gameWindow(game, p, stage_of_action, action,
                            nb_players=nb_players)

        if self.resized_flag:
            self.blit_resized_win()
        else:
            scaled_win = pygame.transform.scale(self.win, self.resized_size)
            self.real_win.blit(scaled_win, (0, 0))

        pygame.display.update()

    def main(self, net, player):
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

        btns_action, btns_card, btns_player, btns_hint_clr, btns_hint_nbr, btns_go_back = game_buttons(
            nb_players=nb_players, player=player)

        while run:
            clock.tick(60)
            # pygame.event.pump()

            game = net.send_data("get")

            self.redrawWindow(game, player, stage_of_action,
                              move[0], nb_players=nb_players)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()

                elif event.type == pygame.VIDEORESIZE:
                    self.resized_size = event.dict['size']
                    self.resized_flag = True

                if game.current_player.index == player:

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = self.scale_pos(pygame.mouse.get_pos())

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
                                if btns_go_back[0].click(pos):
                                    stage_of_action = 0
                                    move[0] = "none"

                            else:
                                for btn in btns_card:
                                    if btn.click(pos):
                                        move.append([int(btn.text) - 1])
                                        game = net.send_data(move)
                                        stage_of_action = 0
                                        move = ['none']

                                if btns_go_back[0].click(pos):
                                    stage_of_action = 0
                                    move[0] = "none"

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

                            if btns_go_back[1].click(pos):
                                stage_of_action = 1

    def redrawMenuWindow(self, menu_type, avail_games=None):
        win = self.win
        window_width, window_height = self.window_width, self.window_height

        win.fill(rgb['background'])
        if menu_type == 'main':

            btn_width = 400
            btn_height = 100
            posx, posy = pos_from_center(
                window_width / 2, window_height / 2, btn_width, btn_height)

            btn_start = infoButton('START NEW GAME', posx, posy,
                                   'start-game', width=btn_width, height=btn_height, fs=30)
            btns = [btn_start]
            for i, game_id in enumerate(avail_games.keys()):
                btn_join = infoButton(f'JOIN GAME {game_id}: {avail_games[game_id].nb_players} player', 50 + 400 * i, 600,
                                      f'join-{game_id}', width=400, fs=30)
                btns.append(btn_join)

        elif menu_type == 'start-game':
            font = pygame.font.SysFont("comicsans", 60)
            s = "Select number of players:"
            s_width, s_height = font.size(s)
            text = font.render(s, 1, rgb['black'])
            posx, posy = pos_from_center(
                window_width / 2, window_height / 4, s_width, s_height)
            win.blit(text, (posx, posy))

            btn_width = 150
            btn_height = 100
            gap = 50
            btn_array_width = 4 * btn_width + 3 * gap
            posx, posy = pos_from_center(
                window_width / 2, window_height / 2, btn_array_width, btn_height)
            btns = [infoButton(str(n), posx + i * (btn_width + gap), posy, f'start-{n}')
                    for i, n in enumerate(range(2, 6))]

        for btn in btns:
            btn.draw(win)

        if self.resized_flag:
            self.blit_resized_win()
        else:
            scaled_win = pygame.transform.scale(self.win, self.resized_size)
            self.real_win.blit(scaled_win, (0, 0))

        pygame.display.update()

        return btns

    def menu_screen(self):
        run = True
        clock = pygame.time.Clock()
        net = Network(self.ip_addr, self.port)

        menu_type = 'main'
        to_get = 'get_avail_games'

        while run:
            clock.tick(60)
            # pygame.event.pump()

            games = net.send_data(to_get)
            btns = self.redrawMenuWindow(menu_type, games)
            btn_info = ''

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()

                elif event.type == pygame.VIDEORESIZE:
                    self.resized_size = event.dict['size']
                    self.resized_flag = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = self.scale_pos(pygame.mouse.get_pos())

                    for btn in btns:
                        if btn.click(pos):
                            btn_info = btn.click(pos)

                    if btn_info == 'start-game':
                        menu_type = btn_info

                    elif btn_info.startswith('start'):
                        player = net.send_data(btn_info)
                        print("player received when joining:", player)
                        run = False

                    elif btn_info.startswith('join'):
                        reply = net.send_data(btn_info)
                        if isinstance(reply, int):
                            player = reply
                            print("player received when joining:", player)
                            run = False
                        elif reply == 'choose_again':
                            print('Game is full, choose again')
                            menu_type = 'main'

        # pass control to main
        self.main(net, int(player))


if __name__ == '__main__':
    import sys
    ip_addr = sys.argv[1]
    Client(ip_addr, 5555)
