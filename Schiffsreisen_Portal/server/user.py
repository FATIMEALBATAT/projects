import random
import json

class User():
    realName: str
    username: str
    password: str
    money: int
    picnr: int
    booking: list
    def __init__(self, data):
        self.realName = data.get("realName")
        self.username = data.get("username")
        self.password = data.get("password")
        self.money = data.get("money", 0)
        self.picnr = data.get("picnr", "Blau")
        self.booking = data.get("booking", [])
    def addMoney(self):
        self.money = min(self.money + random.randint(1000,3000), 20000)
    def auth(self, username, password):
        if self.username == username and self.password == password:
            return True
        return False
    def book(self, text={}):
        if text != None:
            self.booking.append(text)
            self.money = self.money - int(text["preis"])
    def deleteBooking(self, text):
        for i in range(len(self.booking)):
            if text == self.booking[i]:
                self.money += self.booking[i]["preis"]
                self.money = min(self.money, 20000)
                self.booking.pop(i)
                break