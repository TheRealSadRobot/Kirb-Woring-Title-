import pygame
import pickle
import socket
import sys

key = "key"
pygame.init()

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
    while True:
        got = connectionHost.recv(5000000000)
        #print(got)
        sentList = pickle.loads(got)
        #print(sentList)
        if sentList[pygame.K_DOWN]:
            print("DOWN")
        """try:
            pass
        except:
            break"""
    connector.close()
    #sys.exit()

