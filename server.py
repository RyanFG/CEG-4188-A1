#Ryan Frost-Garant | 300114543

from socket import *
import threading
import sys

def newConnection(connectionSocket,addr):
    connectionSocket.send("Connected".encode())
    name = connectionSocket.recv(4096).decode()
    currChan = ""
    connectList.append([connectionSocket,name,currChan])

    while True:
        
        received = connectionSocket.recv(4096).decode()

        if(received[:7] == "/create"):
            channelList.append(received[8:])

        elif(received[:5] == "/exit"):
            connectionSocket.close()
            for n in connectList:
                if(connectList[n][1] == name):
                    del connectList[n]
            break

        elif(received[:5] == "/join"):
            currChan = received[6:]
            toSend = name + " has joined"

            included = False
            for c in channelList:
                if(channelList[c] == currChan):
                    included = True
                    for n in connectList:
                        if(connectList[n][1] == name):
                            connectList[n][2] = currChan
                    break

            if(not included):
                toSend = "No channel named"+ currChan + "exists. Try '/create ?"
                connectionSocket.send(toSend.encode())
            else:
                for i in connectList:
                    if(connectList[i][2] == currChan and connectList[i][1] != name):
                        connectList[i][0].send(toSend.encode())

        elif(received[:5] == "/list"):
            #send list of channels to user, for loop?
            toSend = ""
            for c in channelList:
                toSend += channelList[c] + "\n"
            connectionSocket.send(toSend.encode())

        elif(currChan == ""):
            toSend = "Not a valid control message. Valid messages are /create <channel>, /list, and /join <channel>."
            connectionSocket.send(toSend.encode())

        else:
            #send message to all users in currChannel
            toSend = "["+name+"]"+ received
            for i in connectList:
                if(connectList[i][2] == currChan and connectList[i][1] != name):
                    connectList[i][0].send(toSend.encode())

        

        

if(sys.argv < 2):
    print("Usage: python server.py <port>")
    sys.exit(1)


#create server
serverPort = sys.argv[1]
serverName = "127.0.0.1"
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((serverName,serverPort))

channelList = []
connectList = []

serverSocket.listen(5)
while (True):

    connectionSocket, addr = serverSocket.accept()

    if(addr != ""):
        thread = threading.Thread(target=newConnection, args=[connectionSocket,addr])
        thread.start()




