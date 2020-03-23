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


def handle_init(game_pool):
    game, nb_players = None, None

    # Get whether the player wants to create a game or join one
    data = conn.recv(16).decode()
    print(data)

    if data.startswith('start'):
        nb_players = int(data[-1])
        if nb_players in game_pool.keys():
            # Decide how to handle this case (maybe overwrite existing game?)
            print('Game exists')
            game = game_pool[nb_players]
        else:
            print("Creating a new game...")
            game = Hanabi(nb_players)  # TODO change seed for randomness
            game_pool[nb_players] = game
    elif data.startswith('join'):
        nb_players = int(data[-1])
        game = game_pool.get(nb_players, None)  # TODO, handle game not found

    return game, nb_players


def threaded_client(conn, index_player, game_pool):
    game, nb_players = handle_init(game_pool)
    # game = games[4]

    # We send to the client the index of the player
    init_message = f'{index_player}-{nb_players}'.encode()
    print(init_message)
    conn.send(init_message)

    while True:
        # try:
        #     data = pickle.loads(conn.recv(4096*4))
        #     print("received data", data)
        #     if not data:
        #         break
        #
        #     else:
        #         if data != "get":
        #             game.update_table(data)
        #
        #         print("Game to send back:", game)
        #         conn.sendall(pickle.dumps(game))
        # except:
        #     break
        try:
            data = pickle.loads(conn.recv(4096 * 4))
            # print("received data:", data)
        except EOFError:  # ran out of input
            break

        # if data == 'init':

        if data != "get":
            game.update_table(data)

        # print("Game to send back:", game)
        try:
            conn.sendall(pickle.dumps(game))
        except:
            break

    print("Lost connection")
    try:
        del game
        print("Closing Game", 1)
    except:
        pass
    finally:
        conn.close()


game_pool = {}

index_player = 0  # TODO: chango to human readable

while True:
    conn, client_addr = sock.accept()
    # if index_player < 5:  # this assumes specifically 4 person game
    #     print("Connected to:", client_addr)
    #     _thread.start_new_thread(
    #         threaded_client, (conn, index_player, game_pool))
    #     index_player += 1
    # else:
    #     print("Already 4 players in the game")

    # Below is useful for debugging
    print("Connected to:", client_addr)
    _thread.start_new_thread(
        threaded_client, (conn, index_player % 2, game_pool))
    index_player += 1
