import zmq
import pickle
import random
import sys
import time

port = "5050"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://10.142.0.8:%s" % port)

while True:
    p = pickle.dumps("client message to server1")
    p2 = pickle.dumps("client message to server2")
    msg = socket.recv()
    print(msg)
    socket.send(p)
    socket.send(p2)
    time.sleep(1)