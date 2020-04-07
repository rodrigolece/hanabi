import socket
import _thread
import pickle
from struct import pack, unpack

from game import Hanabi

ip_address = "192.168.0.15"
# ip_address = "127.0.0.1"
port = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((ip_address, port))
sock.listen()
print("Server listening, waiting for connection ...")


def send_data(conn, data):
    try:
        pickled_data = pickle.dumps(data)
        # length = len(pickled_data)
        # sendall to make sure it blocks if there's back-pressure on the socket
        length = pack('>Q', len(pickled_data))
        # self.sock.sendall(length)
        conn.sendall(length)
        # self.sock.sendall(pickle.dumps(length))
        # self.sock.sendall(pickled_data)
        conn.sendall(pickled_data)
        # reply = pickle.loads(self.receive_data())
        # return reply
        return None
    except Exception as e:
        print("exception in in server.py send_data")
        print(e)


def receive_data(conn):
    try:
        bs = conn.recv(8)
        (length,) = unpack('>Q', bs)
        # length = pickle.loads(bs)
        # print("length in network receive_data:", length)
        data = b''
        # print("data:", data)
        while len(data) < length:
            # doing it in batches is generally better than trying
            # to do it all in one go, so I believe.
            to_read = length - len(data)
            # print("to_read:", to_read)

            data += conn.recv(
                4096 if to_read > 4096 else to_read)
        #     print("data:", data)
        # print("unpickled data:", pickle.loads(data))
        return pickle.loads(data)
    except Exception as e:
        print("exception in in server.py receive_data")
        print(e)


def threaded_client(conn, client_address):
    global id_new_game

    while True:
        try:
            # data = pickle.loads(conn.recv(2048 * 50))
            data = receive_data(conn)
            # print("data received:", data)

        except EOFError:  # what is this?? raised when the socket is empty and you call recv
            data = ''
            pass

        if not data:
            break

        elif isinstance(data, str):
            if data == "get_avail_games":
                # conn.sendall(pickle.dumps(game_pool))
                avail_game_pool = {}
                for x in game_pool:
                    if game_pool[x]._num_connections < game_pool[x].nb_players:
                        avail_game_pool[x] = game_pool[x]
                # send_data(conn, game_pool)
                send_data(conn, avail_game_pool)

            elif data.startswith('start'):
                print("client_adress:", client_address)
                nb_players = int(data[-1])
                print(
                    f'Creating new game for {nb_players} players. ID: {id_new_game}')
                # TODO change seed for randomness
                game = Hanabi(nb_players, id_new_game)
                p_nbr = 0
                game_pool[id_new_game] = game
                players_connected_to_game[id_new_game] = [client_address]

                ips_p_nbrs[id_new_game] = {client_address[0]: p_nbr}
                print("ips_p_nbrs:", ips_p_nbrs)
                id_game = id_new_game
                id_new_game += 1
                # conn.send(pickle.dumps(p_nbr))
                send_data(conn, p_nbr)

            elif data.startswith('join'):
                id_game = int(data[-1])
                game = game_pool.get(id_game, None)
                if game is not None:
                    nb_connected = len(players_connected_to_game[id_game])
                    # below should have the goal of making sure  there are no problems with two different clients choosing a agme with 1 spot left at roughly the same time
                    if nb_connected < game.nb_players:
                        print("client_adress:", client_address)
                        if client_address[0] in ips_p_nbrs[id_game]:
                            print(
                                f'Re-adding {client_address} to game {id_game}')
                            players_connected_to_game[id_game].append(
                                client_address)
                            game._num_connections = len(
                                players_connected_to_game[id_game])
                            p_nbr = ips_p_nbrs[id_game][client_address[0]]
                        elif len(ips_p_nbrs[id_game]) < game.nb_players:
                            print(f'Adding {client_address} to game {id_game}')
                            players_connected_to_game[id_game].append(
                                client_address)
                            game._num_connections = len(
                                players_connected_to_game[id_game])
                            p_nbr = nb_connected  # player number
                            ips_p_nbrs[id_game][client_address[0]] = p_nbr
                            print("ips_p_nbrs:", ips_p_nbrs)
                        else:
                            send_data(conn, "choose_again")
                            print('Trying to join full game', client_address)
                            continue

                        if game._num_connections == game.nb_players:
                            game._ready = True
                        # conn.sendall(pickle.dumps(p_nbr))
                        send_data(conn, p_nbr)
                    else:
                        # conn.sendall(pickle.dumps("choose_again"))
                        send_data(conn, "choose_again")
                        print('Trying to join full game', client_address)

            elif data == "get":
                try:
                    # conn.sendall(pickle.dumps(game))
                    send_data(conn, game)
                except:
                    break
        else:  # data is not instance of str
            game.update_table(data)
            if game._finished:
                game_pool.pop(game._id_game, None)
                players_connected_to_game.pop(game._id_game, None)
                ips_p_nbrs.pop(game._id_game, None)
                # to do: get rid of ips_p_nbrs dictionary for that game

            try:
                # conn.sendall(pickle.dumps(game))
                send_data(conn, game)
            except:
                break

    print("Lost connection")
    print('Closing connection with:', client_address)
    conn.close()
    if getattr(game, '_finished', 0) is None:  # game hasn't finished
        # Wait for player to come back
        address_list = players_connected_to_game[game._id_game]
        if client_address in address_list:
            address_list.remove(client_address)
        nb_connected = len(address_list)
        game_pool[game._id_game]._num_connections = nb_connected
        if nb_connected == 0:
            game_pool.pop(game._id_game, None)
            players_connected_to_game.pop(game._id_game, None)
            ips_p_nbrs.pop(game._id_game, None)
        elif nb_connected != game_pool[game._id_game].nb_players:
            # TODO: I think this can be done immediately right? no if statement
            game_pool[game._id_game]._ready = False

game_pool = {}
players_connected_to_game = {}
ips_p_nbrs = {}

id_new_game = 0

while True:
    conn, client_addr = sock.accept()
    print("Connected to:", client_addr)

    _thread.start_new_thread(threaded_client, (conn, client_addr))
