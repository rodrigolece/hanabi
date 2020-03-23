import socket
import _thread
import pickle

from game import Hanabi

ip_address = "127.0.0.1"
port = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((ip_address, port))
sock.listen()
print("Waiting for a connection, Server Started")


def threaded_client(conn, index_player, game_num):
    conn.send(str.encode(str(index_player)))

    # maybe a problem? games is defined out of this scope
    game = games[game_num]

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


# initialise game

games = {}
print("Creating a new game...")
games[1] = Hanabi(4)  # this assumes specifically 4 person game

index_player = 1  # human readable

while True:
    conn, client_addr = sock.accept()
    # if index_player < 4:  # this assumes specifically 4 person game
    print("Connected to:", client_addr)
    _thread.start_new_thread(threaded_client, (conn, index_player % 4, 1))
    index_player += 1
    # else:
    #     print("Already 4 players in the game")
