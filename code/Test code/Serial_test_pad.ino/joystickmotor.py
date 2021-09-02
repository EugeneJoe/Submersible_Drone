import pygame
import math
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep
#from robotLib import *

class BoxesGame(ConnectionListener):
    def Network_close(self,data):
        exit()
    def Network_gamepad(self,data):
        if data["type"] == 10:
            if data["info"]["button"] == 3:
                print "Turning Left"
                #stuff to send to arduino
                sleep(1)
            if data["info"]["button"] == 2:
                print "Turning Right"
                #stuff to send to arduino
                sleep(1)           
        if data["type"] == 7:
            if data["info"]["value"] < : #set value
                print "Move Forward"
                #stuff to send to arduino
                sleep(1)
            if data["info"]["value"] > :#set value
                print "Move Backward"
                #stuff to send to arduino
                sleep(1)

    
    def _init_(self):
        address=raw_input("Address of Server: ")
        try:
            if not address:
                host, port="localhost", 8000
            else:
                host,port = address.split(":")
            self.Connect((host, int(port)))
        except:
            print "Error Connecting to Server"
            print "Usage:", "host:port"
            print "e.g", "localhost:31425"
            exit()
        print "Boxes client started"
        self.running = False
        while not self.running:
            self.Pump()
            connection.Pump()
            sleep(0.01)

bg = BoxesGame()
while 1:
    if bg.update()==1:
        break
bg.finished()
