import socket
import pickle
from struct import pack, unpack
import sys


class Network:
    def __init__(self, ip_addr, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip_addr
        self.port = port
        self.addr = (ip_addr, port)

        # Connect the socket as part of initialisation
        self.sock.connect(self.addr)

    def receive_data(self):
        try:
            bs = self.sock.recv(8)
            (length,) = unpack('>Q', bs)
            data = b''
            while len(data) < length:
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
            length = pack('>Q', len(pickled_data))
            self.sock.sendall(length)
            self.sock.sendall(pickled_data)
            reply = self.receive_data()
            return reply
        except Exception as e:
            print("exception in network.py send_data")
            print(e)
