import socket
import threading
import os
import json
from user import *
# https://www.youtube.com/watch?v=FzrlKeYv05M
# https://stackoverflow.com/questions/47539028/transfer-contents-of-a-folder-over-network-by-python

ip = ''
CHUNKSIZE = 1_000_000 # Für Sehr große Dateien
port = 5000
byte_size = 1024
version = "0.0" # Default Wert
userList = []

def prepareData(key, data = None):
    return json.dumps({"key": key, "data": data}).encode()

def getData(data):
    return json.loads(data.decode())

def sendUpdate(client_socket: socket.socket):
    for path,dirs,files in os.walk('files'):
        for file in files:
            filename = os.path.join(path,file)
            relpath = os.path.relpath(filename,'files')
            filesize = os.path.getsize(filename)
            with open(filename,'rb') as f:
                client_socket.send(prepareData("file", {"path": relpath, "filesize": filesize}))
                data = f.read()
                client_socket.send(data)
            answer = getData(client_socket.recv(byte_size))
            if answer["data"]:
                continue
    client_socket.send(prepareData("file"))


def handle_connection(client_socket: socket.socket, client_addr):
    print("Connection build: " ,client_addr)
    try:
        while True:
            action = getData(client_socket.recv(byte_size))
            if action["key"] == "version":
                client_socket.send(prepareData("version", version))
            elif action["key"] == "register":
                nameExists = False
                for i in range(len(userList)):
                    if action["data"]["username"] == userList[i].username:
                        nameExists = True
                if nameExists:
                    client_socket.send(prepareData("registerAnswer", {"success": False, "info":"Benutzername existiert schon"}))
                else:
                    userList.append(User(action["data"]))
                    safeUsers()
                    client_socket.send(prepareData("registerAnswer", {"success": True, "info": "Account wurde erfolgreich erstellt"}))
            elif action["key"] == "auth":
                userExists = -1
                for i in range(len(userList)):
                    if userList[i].auth(action["data"]["username"], action["data"]["password"]):
                        userExists = i
                        break
                if userExists >= 0:
                    userList[userExists].addMoney()
                    safeUsers()
                    client_socket.send(prepareData("authAnswer", userList[userExists].__dict__)) # User exists / Send Current User Data
                else:
                    client_socket.send(prepareData("authAnswer", False)) # User dont exists
            elif action["key"] == "update":
                sendUpdate(client_socket)
            elif action["key"] == "updateUserdata":
                userExists = -1
                for i in range(len(userList)):
                    if userList[i].auth(action["data"]["username"], action["data"]["password"]):
                        userExists = i
                        break
                if userExists >= 0:
                    userList[userExists] = User(action["data"])
                    client_socket.send(prepareData("updateUserdata", userList[userExists].__dict__))
                else:
                    client_socket.send(prepareData("updateUserdata"))
            elif action["key"] == "book":
                userExists = -1
                for i in range(len(userList)):
                    if userList[i].auth(action["data"]["username"], action["data"]["password"]):
                        userExists = i
                        break
                if userExists >= 0:
                    if action["data"]["reise"] != None:
                        userList[userExists].book(action["data"]["reise"])
                        safeUsers()
                    client_socket.send(prepareData("bookAnswer", userList[userExists].__dict__)) # User exists / Send Current User Data
                else:
                    client_socket.send(prepareData("bookAnswer", None)) # User dont exists
            elif action["key"] == "deleteBooking":
                userExists = -1
                for i in range(len(userList)):
                    if userList[i].auth(action["data"]["username"], action["data"]["password"]):
                        userExists = i
                        break
                if userExists >= 0:
                    if action["data"]["reise"] != None:
                        userList[userExists].deleteBooking(action["data"]["reise"])
                        safeUsers()
                    client_socket.send(prepareData("deleteBookingAnswer", userList[userExists].__dict__)) # User exists / Send Current User Data
                else:
                    client_socket.send(prepareData("deleteBookingAnswer", None)) # User dont exists
    except:
        print("Connection closed: " ,client_addr)
    

def safeUsers():
    with open("users.json", "w+") as file:
        file.write(json.dumps([user.__dict__ for user in userList]))

# Loading Users
with open("users.json", "r+") as file:
    userList = []
    temp = json.loads(file.read())
    for i in range(len(temp)):
       userList.append(User(temp[i]))
    print(str(len(temp)) + " User geladen")



# Starting server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((ip, port))
server_socket.listen(1)
print("Starting Server...")
with open("VERSION", "r") as file:
    version = file.read()
    print("Version:", version)

while True:
    (client_socket, client_addr) = server_socket.accept()
    threading.Thread(target=handle_connection, args=(client_socket, client_addr)).start()