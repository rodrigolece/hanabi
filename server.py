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


def threaded_client(conn, game, p_nbr):
    conn.send(str.encode(str(p_nbr)))

    while True:
        try:
            data = pickle.loads(conn.recv(4096 * 4))
            # print("received data:", data)
        except EOFError:
            data = ''
            pass

        if not data:
            break

        else:
            if data != "get":
                game.update_table(data)

            # print("Game to send back:", game)
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
    conn.close()


game_pool = {}
players_connected_to_game = {}

id_new_game = 0

while True:
    conn, client_addr = sock.accept()
    print("Connected to:", client_addr)

    data = ''
    try:
        data = conn.recv(16).decode()
        print('Received init message:', data)
    except:
        print('Problem receiving init message')
        print('Clossing connection with:', client_addr)
        conn.close()

    # only executed when data was read
    if data.startswith('start'):
        nb_players = int(data[-1])
        print(f'Creating new game for {nb_players} players. ID: {id_new_game}')
        game = Hanabi(nb_players)  # TODO change seed for randomness
        p_nbr = 0
        game_pool[id_new_game] = game
        players_connected_to_game[id_new_game] = [client_addr]
        id_new_game += 1

    elif data.startswith('join'):
        close_connection = False
        id_game = int(data[-1])
        game = game_pool.get(id_game, None)
        if game is not None:
            nb_connected = len(players_connected_to_game[id_game])
            if nb_connected < game.nb_players:
                print(f'Adding {client_addr} to game {id_game}')
                players_connected_to_game[id_game].append(client_addr)
                p_nbr = nb_connected
            else:
                print('Game is full')
                close_connection = True
        else:
            print(f'Game {id_game} does not exist')
            close_connection = True

        if close_connection:
            print('Closing connection with:', client_addr)
            conn.close()
            continue

    # only executed if the connection is still in place
    _thread.start_new_thread(threaded_client, (conn, game, p_nbr))

    # Below is useful for debugging, send game as opposed to start threaded_client
    # try:
    #     print('Sending game')
    #     conn.sendall(pickle.dumps(game))
    #
    # except:
    #     print('Problem sending game')
    #     print('Closing connection with:', client_addr)
    #     conn.close()
