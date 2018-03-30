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

#import zmq
import pickle
import threading
import socket
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

# def serverThread():
#     context = zmq.Context()
#     socket = context.socket(zmq.REP)
#     print(ip)
#     socket.bind("tcp://*:%s" % (port2))
#     while True:
#         message = socket.recv()
#         pmessage = pickle.loads(message)
#         print("Received request: ", pmessage)
#         socket.send_string("ACK")
#         #send(ip_dict.get('c1'), "Gotcha")
#         time.sleep(1)

# def clientThread():
#     context = zmq.Context()
#     print("Starting client thread...")
#     socket = context.socket(zmq.REQ)
#     socket.connect("tcp://%s:%s" % (ip,port))

# def send(ip_in, str):
#     context = zmq.Context()
#     socket_1 = context.socket(zmq.REQ)
#     socket_1.connect("tcp://%s:%s" % (ip_in,port))
#     p = pickle.dumps(str)
#     socket_1.send(p)


def serverThread():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', port))
    serversocket.listen(7)  # become a server socket, maximum 7 connections
    while True:
        clientsocket, addr = serversocket.accept()

        print("Got a connection from %s" % str(addr))
        currentTime = time.ctime(time.time()) + "\r\n"
        clientsocket.send(currentTime.encode('ascii'))
        clientsocket.close()

def clientThread():
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(('10.142.0.8', port))
    tm = clientSocket.recv(1024)
    clientSocket.close()
    print("The time got from the server is %s" % tm.decode('ascii'))

if __name__ == '__main__':
    print("Hello World")
    nodeName = sys.argv[1]
    threads = []
    print(nodeName)
    port = 5050
    #port2 = 5051

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

    while True:
        n = input("Enter s to send ")
        #if n is 's':
            #send(ip_dict.get('c2'), "Hello Friend")