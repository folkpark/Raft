import zmq
import pickle
import random
import sys
import time

port = "5000"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://10.142.0.4:%s" % port)

while True:
    p = pickle.dumps("client message to LEADER")
    msg = socket.recv()
    pmessage = pickle.loads(msg)
    print(pmessage)
    socket.send(p)
    time.sleep(1)