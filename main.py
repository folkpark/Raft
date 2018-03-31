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
global role
global leader_ip
global leader_port


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
    socket1 = context.socket(zmq.PAIR)
    socket2 = context.socket(zmq.PAIR)
    socket3 = context.socket(zmq.PAIR)
    socket4 = context.socket(zmq.PAIR)
    if nodeName is 's1':
        socket1.bind("tcp://10.142.0.2:%s" % port_List[0])
        socket2.bind("tcp://10.142.0.2:%s" % port_List[1])
        socket3.bind("tcp://10.142.0.2:%s" % port_List[2])
        socket4.bind("tcp://10.142.0.2:%s" % port_List[3])
    elif nodeName is 's2':
        socket1.bind("tcp://10.142.0.3:%s" % port_List[0])
        socket2.bind("tcp://10.142.0.3:%s" % port_List[4])
        socket3.bind("tcp://10.142.0.3:%s" % port_List[5])
        socket4.bind("tcp://10.142.0.3:%s" % port_List[6])
    elif nodeName is 's3':
        socket1.bind("tcp://10.142.0.4:%s" % port_List[1])
        socket2.bind("tcp://10.142.0.4:%s" % port_List[4])
        socket3.bind("tcp://10.142.0.4:%s" % port_List[7])
        socket4.bind("tcp://10.142.0.4:%s" % port_List[8])
    elif nodeName is 's4':
        socket1.bind("tcp://10.142.0.5:%s" % port_List[2])
        socket2.bind("tcp://10.142.0.5:%s" % port_List[5])
        socket3.bind("tcp://10.142.0.5:%s" % port_List[7])
        socket4.bind("tcp://10.142.0.5:%s" % port_List[9])
    elif nodeName is 's5':
        socket1.bind("tcp://10.142.0.6:%s" % port_List[3])
        socket2.bind("tcp://10.142.0.6:%s" % port_List[6])
        socket3.bind("tcp://10.142.0.6:%s" % port_List[8])
        socket4.bind("tcp://10.142.0.6:%s" % port_List[9])
    while True:
        p = pickle.dumps("Server message to client")
        socket1.send(p)
        socket2.send(p)
        socket3.send(p)
        socket4.send(p)
        message = socket1.recv()
        pmessage = pickle.loads(message)
        print("Received: ", pmessage)
        #send(ip_dict.get('c1'), "Gotcha")
        time.sleep(1)


def clientThread():
    port = port_dict.get('s1')
    print("Port: %s" % port)
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.connect("tcp://10.142.0.2:%s" % port)

    while True:
        msg = socket.recv()
        pmessage = pickle.loads(msg)
        print(pmessage)
        p = pickle.dumps("client message to LEADER")
        socket.send(p)
        time.sleep(1)

# def send(ip_in, str):
#     context = zmq.Context()
#     socket_1 = context.socket(zmq.REQ)
#     socket_1.connect("tcp://%s:%s" % (ip_in,port))
#     p = pickle.dumps(str)
#     socket_1.send(p)


if __name__ == '__main__':
    nodeName = sys.argv[1]
    threads = []
    print("My name is: " + nodeName)

    ip_dict = {
        's1':'10.142.0.2',
        's2':'10.142.0.3',
        's3':'10.142.0.4',
        's4':'10.142.0.5',
        's5':'10.142.0.6',
        'c1':'10.142.0.7',
        'c2':'10.142.0.8'
    }

    port_List = ["5000","5001","5002","5003","5004",
            "5005","5006","5007","5008","5009",]

    port_dict = {}
    if nodeName is 's1':
        port_dict = {
            's2':"5000",
            's3': "5001",
            's4': "5002",
            's5': "5003"
        }
    elif nodeName is 's2':
        port_dict = {
            's1':"5000",
            's3': "5004",
            's4': "5005",
            's5': "5006"
        }
    elif nodeName is 's3':
        port_dict = {
            's1':"5001",
            's2': "5004",
            's4': "5007",
            's5': "5008"
        }
    elif nodeName is 's4':
        port_dict = {
            's1':"5002",
            's2': "5005",
            's3': "5007",
            's5': "5009"
        }
    elif nodeName is 's5':
        port_dict = {
            's1':"5003",
            's2': "5006",
            's3': "5008",
            's4': "5009"
        }

    ip = ip_dict.get(nodeName)
    # leader_ip = ip_dict.get('s1')
    # leader_port = port_dict.get('s1')

    time.sleep(4)
    print("Starting server thread...")
    serverThread = threading.Thread(target=serverThread)
    threads.append(serverThread)
    clientThread = threading.Thread(target=clientThread)
    threads.append(clientThread)
    serverThread.start()
    clientThread.start()
    time.sleep(1) #wait one second for the connections to be made.

