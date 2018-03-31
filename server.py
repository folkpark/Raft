import zmq
import pickle
import random
import sys
import time

port = "5000"
port2 = "5001"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://10.142.0.4:%s" % port)

socket2 = context.socket(zmq.PAIR)
socket2.bind("tcp://10.142.0.4:%s" % port2)

while True:
    p = pickle.dumps("Server message to client3")
    socket.send(p)
    socket2.send(p)
    msg = socket.recv()
    pmessage = pickle.loads(msg)
    print(pmessage)
    time.sleep(1)