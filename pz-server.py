#!/usr/bin/env python -tt

from __future__ import with_statement
from __future__ import print_function

import zmq
import json
import hmac, hashlib
import threading

ctx = zmq.Context(1)

def msg_check_digest(x):
    digester = hmac.new('shared-secret-here', '', hashlib.sha256)
    digester.update(json.dumps(x[0]))
    return digester.hexdigest() == x[1]

server = ctx.socket(zmq.PULL)
server.bind("tcp://*:1928")

def handle_packet(p):
    if msg_check_digest(p):
        with open("/tmp/foo", "a") as pipe:
            pipe.write(json.dumps(p[0]) + "\n")
    print(p)

while True:
    packet = json.loads(server.recv())
    thread = threading.Thread(target=handle_packet, args=[packet])
    thread.daemon = True
    thread.start()
