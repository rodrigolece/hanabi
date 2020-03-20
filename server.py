import socket
from _thread import *
import pickle
from game import Hanabi

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


def threaded_client(conn, p, game_num):
    conn.send(str.encode(str(p)))

    reply = ""
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
        data = pickle.loads(conn.recv(4096*4))
        # print("received data:", data)
        game = games[game_num]
        if not data:
            break

        else:
            if data != "get":
                game.update_table(data)

            print("Game to send back:", game)
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
    conn.close()


# initialise game

games = {}
print("Creating a new game...")
p=0 #first player to connect is player 0
games[1] = Hanabi(4)
while True:
    conn, addr = s.accept()
    if p<=3: #this assumes specifically 4 person game
        print("Connected to:", addr)
        start_new_thread(threaded_client, (conn, p, 1))
        p += 1 #next players number
    else:
        print("Already 4 players in the game")
