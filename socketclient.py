#!/usr/bin/env python

import socket
import json

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
# sock.connect(('10.27.0.182', 8087))
# JSONMessage = {
#     "jsonrpc": "2.0",
#     "method": "UI.OnMicrophoneRecording",
#     "params": {
#         "binary_data": "1" * 10000
#     }
# }
# jsonstr = json.dumps(JSONMessage).replace(" ", "")
# sock.send(jsonstr)
# print sock.recv(10240)
# print '*************'


import websocket
JSONMessage = {
    "jsonrpc": "2.0",
    "method": "UI.OnMicrophoneRecording",
    "params": {
        "binary_data": "1" * 10000
    }
}
jsonstr = json.dumps(JSONMessage).replace(" ", "")
ws = websocket.WebSocket()
ws.connect("ws://10.27.0.182: 8087")
ws.send(jsonstr)
print ws.recv()
