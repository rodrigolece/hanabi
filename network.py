import socket
import pickle


class Network:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "82.14.199.227"  # TODO: remove once we share
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

    def send(self, data):
        try:
            self.sock.send(pickle.dumps(data))
            reply = pickle.loads(self.sock.recv(2048 * 10))
            return reply
        except Exception as e:
            print(e)

    def send_bytes(self, data):
        self.sock.sendall(data)

        return None
