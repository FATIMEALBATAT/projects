import socket
import os
import time
from customtkinter import *
import json
import popup
from files import data

client_socket = socket.socket()

ip = 'localhost'
port = 5000
byte_size = 1024

updated = False
loginUpdated = False
registerUpdate = False

def prepareData(key, data = None):
    return json.dumps({"key": key, "data": data}).encode()

def getData(data):
    return json.loads(data.decode())

def updateLoginData(app):
    global loginUpdated
    data.auth.username = app.screens[2].items[1].get()
    data.auth.password = app.screens[2].items[2].get()
    loginUpdated = True

def logout(app, status: StringVar):
    global client_socket
    data.auth.username = ""
    data.auth.password = ""
    data.userdata["username"] = ""
    data.userdata["password"] = ""
    with open("assets/userdata.json", "w+") as file:
        file.write(json.dumps(data.userdata))
    client_socket.shutdown(2)
    client_socket.close()
    app.destroy()


def register(app):
    global registerUpdate
    realName = app.screens[3].items[1].get()
    username = app.screens[3].items[2].get()
    password = app.screens[3].items[3].get()
    passwordverify = app.screens[3].items[4].get()
    if password == passwordverify:
        data.auth.realName = realName
        data.auth.username = username
        data.auth.password = password
        registerUpdate = True
    else:
        pop = popup.Popup("Passwörter stimmen nicht überein", app.returnCoords(popup.size))

def update(status: StringVar):
    global client_socket
    client_socket.send(prepareData("update"))
    with client_socket,client_socket.makefile('rb') as clientfile:
        while True:
            answer = getData(client_socket.recv(byte_size))
            if answer["data"] != None:
                relpath = answer["data"]["path"]
                filesize = answer["data"]["filesize"]
                status.set("Downloading: " + relpath + "," + str(filesize))
                path = os.path.join('data',relpath)
                os.makedirs(os.path.dirname(path),exist_ok=True)
                with open(path, "wb") as file:
                    file.write(clientfile.read(filesize))
                client_socket.send(prepareData("UpdateNextFile", True))
            else:
                break
    status.set("Updated !")

def requestVersion(currversion,app, status: StringVar):
    global client_socket
    global updated
    client_socket.send(prepareData("version"))
    answer = getData(client_socket.recv(byte_size))
    if answer["data"] != currversion:
        update(status)
        with open("assets/VERSION", "w") as file:
            file.write(answer["data"])
        popup.Popup("Updated v" + answer["data"], app.returnCoords(popup.size))
    updated = True

def updateUserData(userdata, app):
    global client_socket
    client_socket.send(prepareData("updateUserdata", userdata))
    answer = getData(client_socket.recv(byte_size))
    if answer["data"] != None:
        with open("assets/userdata.json", "w+") as file:
            file.write(json.dumps(answer["data"]))
    else:
        popup.Popup("Fehler beim Senden der Userdaten", app.returnCoords(popup.size))

def book(reise):
    global client_socket
    client_socket.send(prepareData("book", {"username": data.auth.username, "password": data.auth.password, "reise": reise}))
    answer = getData(client_socket.recv(byte_size))
    if answer != None:
        with open("assets/userdata.json", "w+") as file:
            file.write(json.dumps(answer["data"]))
            data.userdata = answer["data"]
        return True
    else:
        return False

def deleteBooking(reise):
    global client_socket
    client_socket.send(prepareData("deleteBooking", {"username": data.auth.username, "password": data.auth.password, "reise": reise}))
    answer = getData(client_socket.recv(byte_size))
    if answer != None:
        with open("assets/userdata.json", "w+") as file:
            file.write(json.dumps(answer["data"]))
            data.userdata = answer["data"]
        return True
    else:
        return False

def authentification(app):
    global client_socket
    global loginUpdated
    global registerUpdate
    client_socket.send(prepareData("auth", {"username": data.auth.username, "password": data.auth.password}))
    answer = getData(client_socket.recv(byte_size))
    if answer["data"] == False: # switch to login screen -> wrong data
        app.switchScreen(2)
    loginUpdated = False
    while (answer["key"] == "authAnswer" and answer["data"] != False) == False:
        if loginUpdated:
            client_socket.send(prepareData("auth", {"username": data.auth.username, "password": data.auth.password}))
            answer = getData(client_socket.recv(byte_size))
            if answer["data"] == False:
                popup.Popup("Login fehlgeschlagen", app.returnCoords(popup.size))
            loginUpdated = False
        elif registerUpdate:
            client_socket.send(prepareData("register", {"realName":data.auth.realName,"username": data.auth.username, "password": data.auth.password}))
            answer = getData(client_socket.recv(byte_size))
            popup.Popup(answer["data"]["info"], app.returnCoords(popup.size))
            registerUpdate = False
            if answer["data"]["success"]:
                app.switchScreen(2)
        else:
            time.sleep(0.5)
    with open("assets/userdata.json", "w+") as file:
        file.write(json.dumps(answer["data"]))
        data.userdata = answer["data"]

def connectStart(currversion, status: StringVar, app):
    global client_socket
    try:
        client_socket.connect((ip,port))
        requestVersion(currversion, app, status)
        authentification(app)
    except: # https://instructobit.com/tutorial/101/Reconnect-a-Python-socket-after-it-has-lost-its-connection
        client_socket = socket.socket()
        status.set("Network Error")
        connected = False
        for i in range(0, 4):  # 3 Versuche die Verbindung neue aufzubauen
            try:
                client_socket.connect((ip,port))
                status.set("Reconnected")
                connected = True
                break
            except socket.error:
                time.sleep(0.5)
                status.set("Trying to reconnect: Attempt #" + str(i+1))
        if connected:
            if updated == False:
                requestVersion(currversion, app, status)
            authentification(app)
        else:
            status.set("Could not reach network")