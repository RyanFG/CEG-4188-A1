#Ryan Frost-Garant | 300114543

from socket import *
import sys

if(sys.argv < 4):
    print("Usage: python client.py <name> <server> <port>")
    sys.exit(1)

serverName = sys.argv[2]    #localhost
serverPort = sys.argv[3]    #server port

#create socket
clientSocket = socket(AF_INET, SOCK_STREAM)     #for tcp socket

#connect to server
clientSocket.connect((serverName,serverPort))

#create username
username = sys.argv[1]
clientSocket.send(username.encode())    

#receive text from server and print
receivedText = clientSocket.recv(4096)      #4096 = numbr of bytes to receive
print (receivedText.decode())

while(True):
    text = input("[Me] ")
    clientSocket.send(text.encode())

    if(text == "exit"):
        clientSocket.close()
        break

    receivedText = clientSocket.recv(4096)
    print (receivedText.decode())