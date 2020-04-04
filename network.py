import socket
import pickle
from struct import pack, unpack
import sys


class Network:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "82.14.199.227"  # TODO: remove once we share
        # self.server = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        # self.p = self.connect()
        # above doesn't work anymore because we send things before the index

        # Connect the socket as part of initialisation
        self.sock.connect(self.addr)

    # def getP(self):
    #     return self.p

    # def connect(self):
    #     try:
    #         self.sock.connect(self.addr)
    #         return self.sock.recv(2048).decode()
    #     except:
    #         pass

    # def send(self, data):
    #     try:
    #         self.sock.send(pickle.dumps(data))
    #         reply = pickle.loads(self.sock.recv(2048 * 50))
    #         return reply
    #     except Exception as e:
    #         print(e)
    #
    # def send_bytes(self, data):
    #     self.sock.sendall(data)
    #
    #     return None
    #
    def receive_data(self):
        try:
            bs = self.sock.recv(8)

            # print("sys.sizeof bs",sys.getsizeof(bs))

            (length,) = unpack('>Q', bs)
            # length = pickle.loads(bs)

            # print("length in network receive_data:", length)
            data = b''
            # doing it in batches is generally better than trying
            while len(data) < length:
                # to do it all in one go, so I believe.
                to_read = length - len(data)
                data += self.sock.recv(
                    4096 if to_read > 4096 else to_read)
            return pickle.loads(data)
        except Exception as e:
            print("exception in network.py receive_data")
            print(e)

    def send_data(self, data):
        try:
            pickled_data = pickle.dumps(data)
            # length = len(pickled_data)
            # print("data:", data)
            # print("len(pickled_data):", len(pickled_data))
            length = pack('>Q', len(pickled_data))
            # length = len(pickled_data)
            # print("length:", length)
            # sendall to make sure it blocks if there's back-pressure on the socket
            # self.sock.sendall(pickle.dumps(length))
            self.sock.sendall(length)
            # print("network.py sent length")
            # print("pickled data to send:", pickled_data)
            self.sock.sendall(pickled_data)
            # print("sent pickled data in server send_data")
            reply = self.receive_data()
            return reply
        except Exception as e:
            print("exception in network.py send_data")
            print(e)
