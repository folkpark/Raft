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
import datetime
import random
from google.cloud import storage

global ip
global port
global nodeName #My nodename
global role
global leader
global p1_state
global p2_state
# global leader_ip
# global leader_port


# This function is a code same on how to upload a file to
# secure storage on google's cloud services.

def upload_to_cloud(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))


def write_log_to_stable_storage(logEntry):
    file = open("log.txt", "a")
    #write the log out to a file
    file.write('\n')
    file.write(logEntry)
    file.close()
    #upload_to_cloud(bucket, "log.txt", "log.txt")

def serverThread():
    global beginSec
    global endSec
    global p1_state
    global p2_state
    context = zmq.Context()
    socket1 = context.socket(zmq.PAIR)
    socket2 = context.socket(zmq.PAIR)
    socket3 = context.socket(zmq.PAIR)
    socket4 = context.socket(zmq.PAIR)
    socket5 = context.socket(zmq.PAIR)
    socket6 = context.socket(zmq.PAIR)
    if nodeName == 's1':
        socket1.bind("tcp://10.142.0.2:%s" % port_List[0])
        socket2.bind("tcp://10.142.0.2:%s" % port_List[1])
        socket3.bind("tcp://10.142.0.2:%s" % port_List[2])
        socket4.bind("tcp://10.142.0.2:%s" % port_List[3])
        socket5.bind("tcp://10.142.0.2:%s" % port_List[10])
        socket6.bind("tcp://10.142.0.2:%s" % port_List[11])
    elif nodeName == 's2':
        socket1.bind("tcp://10.142.0.3:%s" % port_List[0])
        socket2.bind("tcp://10.142.0.3:%s" % port_List[4])
        socket3.bind("tcp://10.142.0.3:%s" % port_List[5])
        socket4.bind("tcp://10.142.0.3:%s" % port_List[6])
    elif nodeName == 's3':
        socket1.bind("tcp://10.142.0.4:%s" % port_List[1])
        socket2.bind("tcp://10.142.0.4:%s" % port_List[4])
        socket3.bind("tcp://10.142.0.4:%s" % port_List[7])
        socket4.bind("tcp://10.142.0.4:%s" % port_List[8])
    elif nodeName == 's4':
        socket1.bind("tcp://10.142.0.5:%s" % port_List[2])
        socket2.bind("tcp://10.142.0.5:%s" % port_List[5])
        socket3.bind("tcp://10.142.0.5:%s" % port_List[7])
        socket4.bind("tcp://10.142.0.5:%s" % port_List[9])
    elif nodeName == 's5':
        socket1.bind("tcp://10.142.0.6:%s" % port_List[3])
        socket2.bind("tcp://10.142.0.6:%s" % port_List[6])
        socket3.bind("tcp://10.142.0.6:%s" % port_List[8])
        socket4.bind("tcp://10.142.0.6:%s" % port_List[9])
    elif nodeName == 'c1':
        socket1.bind("tcp://10.142.0.7:%s" % port_List[10])
    elif nodeName == 'c2':
        socket1.bind("tcp://10.142.0.8:%s" % port_List[11])
    event = 1

    if nodeName != 'c1' and nodeName != 'c2':
        while True:
            # print("Inside Server Thread Loop")
            event +=1
            strEvent = str(event)
            # toFollowerMsg = "Leader to follower: event %s" % (strEvent)
            # p = pickle.dumps(toFollowerMsg)
            # socket1.send(p)
            # socket2.send(p)
            # socket3.send(p)
            # socket4.send(p)
            # socket5.send(p)
            # socket6.send(p)
            #write_log_to_stable_storage(toFollowerMsg+"committed")

            message = socket5.recv() #PLayer 1 sent command here
            pmessage = pickle.loads(message)
            action, location = pmessage.split("_")

            if action == 'PUNCH' and p2_state== 'open':
                rand = randomNum()
                if rand == 10:
                    print("HIT HIT HIT")
                    p = pickle.dumps("HEADPOP")
                    socket6.send(p)
                    p = pickle.dumps("Winner")
                    currentTime = datetime.datetime.now()
                    write_log_to_stable_storage("Player 1 punch HIT AND WINS:%s" % currentTime)
                    socket5.send(p)
                    break
                else:
                    print("Player 1 punched MISSED player 2")
                    currentTime = datetime.datetime.now()
                    write_log_to_stable_storage("Player 1 punched MISSED player 2:%s"%currentTime)
                    p = pickle.dumps("Miss!")
                    socket5.send(p)
            elif action == 'PUNCH' and p2_state != 'open':
                print("Punch blocked!!!")
                currentTime = datetime.datetime.now()
                write_log_to_stable_storage("Player 1 punched BLOCKED by player 2:%s" % currentTime)
                p = pickle.dumps("Blocked!!!")
                socket5.send(p)
            elif action == 'BLOCK':
                p1_state = "blocking"
                currentTime = datetime.datetime.now()
                beginSec = currentTime.second
                endSec = beginSec+3
                p = pickle.dumps("You are blocking")
                write_log_to_stable_storage("Player 1 BLOCKING:%s" % currentTime)
                socket5.send(p)


            message = socket6.recv() #Player two sent command here
            pmessage = pickle.loads(message)
            action, location = pmessage.split("_")

            if action == 'PUNCH' and p1_state == 'open':
                rand = randomNum()
                if rand == 10:
                    print("HIT HIT HIT")
                    p = pickle.dumps("HEADPOP")
                    socket5.send(p)
                    p = pickle.dumps("Winner")
                    currentTime = datetime.datetime.now()
                    write_log_to_stable_storage("Player 2 punch HIT AND WINS:%s" % currentTime)
                    socket6.send(p)
                    break
                else:
                    print("Player 2 punch MISSED player 1")
                    currentTime = datetime.datetime.now()
                    write_log_to_stable_storage("Player 2 punch MISSED:%s" % currentTime)
                    p = pickle.dumps("Miss!")
                    socket6.send(p)
            elif action == 'PUNCH' and p1_state != 'open':
                print("Punch blocked!!!")
                currentTime = datetime.datetime.now()
                write_log_to_stable_storage("Player 2 punch BLOCKED by Player 1:%s" % currentTime)
                p = pickle.dumps("Blocked!!!")
                socket6.send(p)
            elif action == 'BLOCK':
                p1_state = "blocking"
                currentTime = datetime.datetime.now()
                beginSec = currentTime.second
                endSec = beginSec + 3
                p = pickle.dumps("You are blocking")
                write_log_to_stable_storage("Player 2 BLOCKING:%s" % currentTime)
                socket6.send(p)

            # message = socket1.recv()
            # pmessage = pickle.loads(message)
            # print("Received: ", pmessage)
            #
            # message = socket2.recv()
            # pmessage = pickle.loads(message)
            # print("Received: ", pmessage)
            #
            # message = socket3.recv()
            # pmessage = pickle.loads(message)
            # print("Received: ", pmessage)
            #
            # message = socket4.recv()
            # pmessage = pickle.loads(message)
            # print("Received: ", pmessage)

            time.sleep(0.5)

            #set the appropriate states for blocking
            currentTime = datetime.datetime.now()
            currentSec = currentTime.second
            if p1_state != 'open' and currentSec >= endSec:
                p1_state = "open"
            if p2_state != 'open' and currentSec >= endSec:
                p2_state = "open"
    print("-----Game over------")

def clientThread():
    port = port_dict.get('s1')
    ip = ip_dict.get('s1')
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    if nodeName != 's1':
        socket.connect("tcp://%s:%s" % (ip,port))


    while role != 'Leader':
        action = printMenu()
        if action == '1':
            p = pickle.dumps("PUNCH_LEFT")
        elif action == '2':
            p = pickle.dumps("PUNCH_RIGHT")
        elif action == '3':
            p = pickle.dumps("BLOCK_LEFT")
        elif action == '4':
            p = pickle.dumps("BLOCK_RIGHT")

        print("sending to leader")
        socket.send(p)
        # if nodeName != 'c1' or nodeName != 'c2':
        #     write_log_to_stable_storage(pmessage)
        msg = socket.recv()
        result = pickle.loads(msg)
        # print("Received: ", pmessage)
        if result == 'Winner':
            print("You knocked off opponents head and WIN!!!")
            break
        elif result == 'HEADPOP':
            print("Your head was knocked off and you LOSE!!!")
            break
        time.sleep(1)
    if role != 'Leader':
        print("-----Game over------")

def printMenu():
    print("############## FIGHT!!! ###########")
    print("Punch Left 1:")
    print("Punch Right 2:")
    print("Block Left 3:")
    print("Block Right 4:")
    n = input("Please enter selection: ")
    return n

#generate random number between 1-10
def randomNum():
    rand = random.randint(1,10)
    return rand

# leader must not be None at the end of this function
def election():
    global leader
    global role
    print("No leader known! Starting election protocol")

    context = zmq.Context()
    socket1 = context.socket(zmq.PAIR)
    socket2 = context.socket(zmq.PAIR)
    socket3 = context.socket(zmq.PAIR)
    socket4 = context.socket(zmq.PAIR)
    count = 0
    connections = []
    socket_List = []
    for key in port_dict:
        tempIP = ip_dict.get(key)
        tempPort = ip_dict.get(key)
        if count is 0:
            socket1.connect("tcp://%s:%s" % (tempIP,tempPort))
            connections.append((key, 1))
            socket_List.append(socket1)
        elif count is 1:
            socket2.connect("tcp://%s:%s" % (tempIP, tempPort))
            connections.append((key, 2))
            socket_List.append(socket2)
        elif count is 2:
            socket3.connect("tcp://%s:%s" % (tempIP, tempPort))
            connections.append((key, 3))
            socket_List.append(socket3)
        elif count is 3:
            socket4.connect("tcp://%s:%s" % (tempIP, tempPort))
            connections.append((key, 4))
            socket_List.append(socket4)
        count += 1


    #Loop with random timer
    #If no candidate messages received, then send out
    #request for votes. Vote for self. If votes is 3 or
    #greater than send out a victory message.

    start_timer = time.time()
    randTimeValue = random.uniform(1.0, 5.0)

    end_timer = start_timer + randTimeValue
    leader = None
    timedOut = False
    voteCount = 1 #One because you vote for self
    voted = False
    while leader == None:
        currentTime = time.time()
        if currentTime >= end_timer:
            timedOut = True

        if timedOut:
            print("Time Out!")
            role = "candidate"
            # ASK for votes
            campaignMessage = "vote_%s" % (nodeName)
            p = pickle.dumps(campaignMessage)
            socket1.send(p)
            socket2.send(p)
            socket3.send(p)
            socket4.send(p)

            #Count the votes
            msg = socket1.recv()
            pmessage = pickle.loads(msg)
            if pmessage == "vote":
                voteCount += 1

            msg = socket2.recv()
            pmessage = pickle.loads(msg)
            if pmessage == "vote":
                voteCount += 1

            msg = socket3.recv()
            pmessage = pickle.loads(msg)
            if pmessage == "vote":
                voteCount += 1

            msg = socket4.recv()
            pmessage = pickle.loads(msg)
            if pmessage == "vote":
                voteCount += 1

            if voteCount >= 3:
                leader = nodeName
                #Send victory message
                p = pickle.dumps("victory_%s" % (nodeName))
                socket1.send(p)
                socket2.send(p)
                socket3.send(p)
                socket4.send(p)

        elif timedOut == False:
            time.sleep(0.25)
            print(".", end='', flush=True)


            msg = socket1.recv()
            pmessage = pickle.loads(msg)
            a,b = pmessage.split("_")
            if a == "victory": #another leader was declared
                leader = b
                break
            elif a == "vote" and voted == False: #give the candidate your vote
                p = pickle.dumps("vote")
                socket1.send(p)
                voted = True

            msg = socket2.recv()
            pmessage = pickle.loads(msg)
            a,b = pmessage.split("_")
            if a == "victory": #another leader was declared
                leader = b
                break
            elif a == "vote" and voted == False: #give the candidate your vote
                p = pickle.dumps("vote")
                socket2.send(p)
                voted = True

            msg = socket3.recv()
            pmessage = pickle.loads(msg)
            a,b = pmessage.split("_")
            if a == "victory": #another leader was declared
                leader = b
                break
            elif a == "vote" and voted == False: #give the candidate your vote
                p = pickle.dumps("vote")
                socket3.send(p)
                voted = True

            msg = socket4.recv()
            pmessage = pickle.loads(msg)
            a,b = pmessage.split("_")
            if a == "victory": #another leader was declared
                leader = b
                break
            elif a == "vote" and voted == False: #give the candidate your vote
                p = pickle.dumps("vote")
                socket4.send(p)
                voted = True

    # time.sleep(4)
    socket_Leader = context.socket(zmq.PAIR)
    port = port_dict.get(leader)
    ip = ip_dict.get(leader)
    socket_Leader.connect("tcp://%s:%s" % (ip, port))
    return socket_Leader

if __name__ == '__main__':
    nodeName = sys.argv[1]
    threads = []
    p1_state = "open"
    p2_state = "open"
    if nodeName == 's1':
        role = "Leader"
    else:
        role = "Follower"
    global leader  # String value of who the leader is
    print("My name is: " + nodeName)
    print("My role is: " + role)
    leader = 's1'
    bucket = None

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
            "5005","5006","5007","5008","5009","6000",
                 "6001"]
    port_dict = {}
    if nodeName == "s1":
        bucket = "s1_bucket"
        port_dict = {
            's2':"5000",
            's3': "5001",
            's4': "5002",
            's5': "5003"
        }
    elif nodeName == 's2':
        bucket = "s1_bucket"
        port_dict = {
            's1':"5000",
            's3': "5004",
            's4': "5005",
            's5': "5006"
        }
    elif nodeName == 's3':
        bucket = "s3_buck"
        port_dict = {
            's1':"5001",
            's2': "5004",
            's4': "5007",
            's5': "5008"
        }
    elif nodeName == 's4':
        bucket = "s4_bucket"
        port_dict = {
            's1':"5002",
            's2': "5005",
            's3': "5007",
            's5': "5009"
        }
    elif nodeName == 's5':
        bucket = "s5_bucket"
        port_dict = {
            's1':"5003",
            's2': "5006",
            's3': "5008",
            's4': "5009"
        }
    elif nodeName == 'c1':
        port_dict = {
            's1':"6000"
        }
    elif nodeName == 'c2':
        port_dict = {
            's1':"6001",
        }

    #make sure the log is clear.
    with open('log.txt', 'w'):
        pass

    time.sleep(3)
    print("Starting server thread...")
    serverThread = threading.Thread(target=serverThread)
    threads.append(serverThread)
    clientThread = threading.Thread(target=clientThread)
    threads.append(clientThread)
    serverThread.start()
    clientThread.start()
    time.sleep(1) #wait one second for the connections to be made.
