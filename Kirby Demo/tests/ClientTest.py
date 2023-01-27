import pygame
import threading
import socket
import sys
import pickle

def connectortest():
    connector = socket.socket()
    connector.settimeout(1000)
    global connectionNum
    global connected
    while connected == False:
        try:
            newAddress = f"192.168.1.{num}"
            #print(newAddress)
            connector.connect((newAddress,thisPort))
            print(newAddress)
            connector.send(key.encode())
            if(connector.recv(1024)).decode() == "Connection Successful":
                print("Connection Established")
                connected = True
                connectionNum = newAddress
                connector.close()
        except Exception as e:
            break
    sys.exit()
            #connector.close()"""

key = "key"
pygame.init()
screenscale = 3
winsizex = 256
winsizey = 240window = pygame.display.set_mode((winsizex*screenscale,winsizey*screenscale))
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
        thread = threading.Thread(target = connectortest)
        thread.start()

while connected == False:
    pass

print("next phase reached")
connector.settimeout(100)
connector.connect((connectionNum,thisPort))
while True:
    pygame.event.get()
    keys = pygame.key.get_pressed()
    message = pickle.dumps(keys)
    #print(message)
    connector.send(message)
    frame = connector.recv(5000)
    window.blit(pygame.transform.scale(displayPane, (winsizex*screenscale,winsizey*screenscale)), (0,0))
    #put the stuff from the frame onto the window
    pygame.display.flip()
connector.close()
print("END OF LINE")
sys.exit()

