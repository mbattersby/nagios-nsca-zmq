#!/usr/bin/env python -tt

from __future__ import with_statement
from __future__ import print_function

import zmq
import json
import time
import hmac, hashlib
import threading

ctx = zmq.Context(1)

def msg_check_digest(packet):
    sent_digest = packet.pop()

    digester = hmac.new('shared-secret-here', '', hashlib.sha256)
    digester.update(json.dumps(packet))
    local_digest = digester.hexdigest()

    sent_time = packet.pop()
    local_time = time.time()

    return sent_digest == local_digest and abs(sent_time - local_time) < 5

server = ctx.socket(zmq.PULL)
server.bind("tcp://*:1928")

def handle_packet(p):
    if msg_check_digest(p):
        with open("dummy.out", "a") as pipe:
            pipe.write(json.dumps(p[0]) + "\n")
    print(p[0])

while True:
    packet = json.loads(server.recv())
    thread = threading.Thread(target=handle_packet, args=[packet])
    thread.daemon = True
    thread.start()
