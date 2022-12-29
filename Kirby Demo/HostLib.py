import pygame
import pickle
import socket
import threading
import sys
from functools import partial

key = "key"
def connectortest(num,thisPort,adr):
    connector = socket.socket()
    connector.settimeout(1000)
    global connectionNum
    global connected
    while connected == False:
        try:
            #print(num)
            newAddress = f"{adr}.{num}"
            print(newAddress)
            connector.connect((newAddress,thisPort))
            print("dip")
            print(newAddress)
            connector.send(key.encode())
            print("dip")
            if(connector.recv(1024)).decode() == "Connection Successful":
                print("Connection Established")
                connected = True
                connectionNum = newAddress
                connector.close()
        except Exception as e:
            break
    sys.exit()
def connect(hostvar):
    if hostvar == 1:
        print("Waiting For connection...")
        thisPC = socket.gethostname()
        thisPort = 3
        connector = socket.socket()
        connector.bind((thisPC,thisPort))
        connector.listen(8)
        connectionHost, otherPC = connector.accept()
        if (connectionHost.recv(1024)).decode() == key:
            print("Connection Established")
            connectionHost.send("Connection Successful".encode())
            connectionHost, otherPC = connector.accept()
            return connectionHost
    else:
        print("Waiting For connection...")
        thisPC = socket.gethostname()
        HostAddress = socket.gethostbyname(thisPC)
        Address = HostAddress.split(".")
        del Address[-1]
        thisPort = 3
        global connected
        global connectionNum
        connectionNum = "Null"
        connector = socket.socket()
        connector.settimeout(1)
        connected = False
        for num in range(1,256):
            if connected == False:
                thread = threading.Thread(target = partial(connectortest,num,thisPort,f"{Address[0]}.{Address[1]}.{Address[2]}"))
                thread.start()
        while connected == False:
            pass
        connector.connect((connectionNum,thisPort))
        return connector

        
def loop(connectionHost):
    got = connectionHost.recv(50000)
    #print(got)
    sentList = pickle.loads(got)
    #print(sentList)
    return sentList
def sendToClient(obj,connectionHost):
    data = pickle.dumps(obj)
    connectionHost.send(data)
    

