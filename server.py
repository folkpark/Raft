import zmq
import random
import sys
import time

port = "5050"
context = zmq.Context()
socket = context.socket(zmq.ROUTER)
time.sleep(2)
socket.connect("tcp://10.142.0.8:%s" % port)

while True:
    socket.send_string("Server message to client3")
    msg = socket.recv()
    print(msg)
    time.sleep(1)