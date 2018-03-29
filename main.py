'''
Author: Parker FOlkman
Date: 3/28/2017
Description: This is a Rock Em Sock Em Robots
game programed to use Google CLoud services in a 
distributed way. Raft is implemented for the consensus
protocol. 

Google CLoud Stable Storage:
https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/storage/cloud-client/snippets.py

'''

import zmq
import pickle
import threading
import time
import sys
#from google.cloud import storage

global ip
global port
global nodeName


# This function is a code same on how to upload a file to
# secure storage on google's cloud services.
'''
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))
'''

def serverThread():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    print(ip)
    socket.bind("tcp://%s:%s" % (ip,port))
    while True:
        message = socket.recv()
        pmessage = pickle.loads(message)
        print("Received request: ", pmessage)
        time.sleep(1)

def clientThread():
    context = zmq.Context()
    print("Starting client thread...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://%s:%s" % (ip,port))

def send():
    context = zmq.Context()
    socket_1 = context.socket(zmq.REQ)
    ip_c2 = '10.142.0.8'
    socket_1.connect("tcp://%s:%s" % (ip_c2,port))
    p = pickle.dumps("Hello Friend")

    socket_1.send(p)

if __name__ == '__main__':
    print("Hello World")
    nodeName = sys.argv[1]
    threads = []
    print(nodeName)
    port = 20 #next try 20

    ip_dict = {
        's1':'10.142.0.2',
        's2':'10.142.0.3',
        's3':'10.142.0.4',
        's4':'10.142.0.5',
        's5':'10.142.0.6',
        'c1':'10.142.0.7',
        'c2':'10.142.0.8'
    }

    ip = ip_dict.get(nodeName)

    serverThread = threading.Thread(target=serverThread)
    threads.append(serverThread)
    clientThread = threading.Thread(target=clientThread)
    threads.append(clientThread)
    serverThread.start()
    clientThread.start()
    time.sleep(1) #wait one second for the connections to be made.

    n = input("Enter s to send ")
    if n is 's':
        send()