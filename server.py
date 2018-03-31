import zmq
import pickle
import random
import sys
import time

port = "5050"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://10.142.0.8:%s" % port)

while True:
    p = pickle.dumps("Server message to client3")
    socket.send(p)
    msg = socket.recv()
    print(msg)
    time.sleep(1)