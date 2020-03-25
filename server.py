import socket
import _thread
import pickle

from game import Hanabi

ip_address = "127.0.0.1"
port = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((ip_address, port))
sock.listen()
print("Server listening, waiting for connection ...")


def threaded_client(conn, client_address):
    global id_new_game

    while True:
        try:
            data = pickle.loads(conn.recv(4096 * 4))

        except EOFError:  # what is this?? raised when the socket is empty and you call recv
            data = ''
            pass

        if not data:
            break

        elif isinstance(data, str):
            if data == "get_avail_games":
                conn.sendall(pickle.dumps(game_pool))

            elif data.startswith('start'):
                nb_players = int(data[-1])
                print(
                    f'Creating new game for {nb_players} players. ID: {id_new_game}')
                game = Hanabi(nb_players)  # TODO change seed for randomness
                p_nbr = 0
                game_pool[id_new_game] = game
                players_connected_to_game[id_new_game] = [client_address]
                id_game = id_new_game
                id_new_game += 1
                conn.send(pickle.dumps(p_nbr))

            elif data.startswith('join'):
                id_game = int(data[-1])
                game = game_pool.get(id_game, None)
                if game is not None:
                    nb_connected = len(players_connected_to_game[id_game])
                    # below should have the goal of making sure  there are no problems with two different clients choosing a agme with 1 spot left at roughly the same time
                    if nb_connected < game.nb_players:
                        print(f'Adding {client_addr} to game {id_game}')
                        players_connected_to_game[id_game].append(
                            client_address)
                        game._num_connections += 1
                        p_nbr = nb_connected  # player number
                        if game._num_connections == game.nb_players:
                            game._ready = True
                        conn.sendall(pickle.dumps(p_nbr))
                    else:
                        conn.sendall(pickle.dumps("choose_again"))
                        print('Trying to join full game', client_addr)

            elif data == "get":
                try:
                    conn.sendall(pickle.dumps(game))
                except:
                    break
        else:  # data is not instance of str
            game.update_table(data)

            try:
                conn.sendall(pickle.dumps(game))
            except:
                break

    print("Lost connection")
    # TODO This needs to be done more carefully, probably outside the thread
    # try:
    #     del game
    #     print("Closing Game", 1)
    # except:
    #     pass
    print('Closing connection with:', client_addr)
    conn.close()
    players_connected_to_game[id_game].remove(client_addr)


game_pool = {}
players_connected_to_game = {}

id_new_game = 0

while True:
    conn, client_addr = sock.accept()
    print("Connected to:", client_addr)

    _thread.start_new_thread(threaded_client, (conn, client_addr))
