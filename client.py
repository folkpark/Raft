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
    msg = socket.recv()
    print(msg)
    socket.send_string("heartbeat")
    socket.send_string("client message to server2")
    time.sleep(1)