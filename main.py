#!/usr/bin/env python3

import argparse

from client import Client

parser = argparse.ArgumentParser(description='Hanabi Client')
parser.add_argument('-i', '--ipaddr', dest='ip_addr', default="82.14.199.227",
                    help='The IP address of the game server')
# parser.add_argument('ip_addr', help='The IP address of the game server')
parser.add_argument('-l', '--local', action='store_const', const=True, default=False,
                    help='Use the default local IP address (not localhost)')
parser.add_argument('-p', '--port', type=int, default=5555,
                    help='The port to use (default is 5555)')
args = parser.parse_args()

try:
    ip_addr = args.ip_addr if args.local is False else "192.168.0.15"
    port = args.port
    print(f'Staring client connecting to {ip_addr}:{port}')
    Client(ip_addr, port)
except Exception as e:
    print("exception starting the client")
    print(e)
