#!/usr/bin/env python

from __future__ import with_statement

import sys
import zmq
import json
import hmac, hashlib

class PZClient:
    def __init__(self, configfile=False):
        if configfile:
            self.secret = self.read_secret(configfile)
        else:
            self.secret = 'shared-secret-here'

    def read_secret(self, filename):
        with open(filename, "r") as f:
            for l in iter(f.readline, b''):
                l = l.rstrip("\r\n")
                if l.startswith('#') or l == "":
                    continue
                setting = l.split('=', 2)
                if setting and setting[0] == 'password':
                    return setting[1]

    def payload_digest(self, x):
        digester = hmac.new(self.secret, '', hashlib.sha256)
        digester.update(json.dumps(x))
        return digester.hexdigest()

    def send(self, packet):
        client = zmq.Context(1).socket(zmq.PUSH)
        client.connect('tcp://localhost:1928')
        client.send(json.dumps([ packet, self.payload_digest(packet) ]))

pz = PZClient(
pz.send(sys.argv)
