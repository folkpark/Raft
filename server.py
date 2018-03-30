import zmq
import random
import sys
import time

port = "5050"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
time.sleep(2)

while True:
    socket.connect("tcp://10.142.0.8:%s" % port)
    socket.send_string("Server message to client3")
    msg = socket.recv()
    print(msg)
    time.sleep(1)