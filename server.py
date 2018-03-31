import zmq
import pickle
import random
import sys
import time

port = "5060"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://10.142.0.3:%s" % port)

while True:
    p = pickle.dumps("Server message to client3")
    socket.send(p)
    msg = socket.recv()
    pmessage = pickle.loads(msg)
    print(pmessage)
    time.sleep(1)