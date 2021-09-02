import PodSixNet.Server
from pygame import *
from time import sleep
init()

class ClientChannel(PodSixNet.Channel.Channel):
    def Network(self,data):
        print data
    def Close(self):
        self._server.close(self.gameid)
class BoxesServer(PodSixNet.Server.Server):

    channelClass = ClientChannel
    def _init_(self, *args, **kwargs):
        PodSixNet.Server.Server._init_(self, *args, **kwargs)
        self.games = []
        self.queue = None
        self.currentIndex = 0
    def Connected(self, channel, addr):
        print 'new connection:', channel
        if self.queue == None:
            self.currentIndex+=1
            channel.gameid = self.currentIndex
            self.queue = Game(channel, self.currentIndex)
    def close(self, gameid):
        try:
            game = [a for a in self.games if a.gameid==gameid][0]
            game.player0.Send({"action":"close"})
        except:
            pass
    def tick(self):
        if self.queue != None:
            sleep(.05)
            for e in event.get():
                self.queue.player0.Send({"action":"gamepad", "type":e.type})
        self.pump()
class Game:
    def _init_(self, player0, currentIndex):
        self.player0 = player0

###Setup and init joystick
##j = joystick.Joystick(0)
##j.init()

###check init status
##if j.get_init() == 1:
##    print "Joystick in initialized"
##
###Get and print joystick ID
##print "Joystick ID: ", j.get_name()
##
###Get and print number of buttons
##print "No. of buttons: ", j.get_numbuttons()
##
###Get and print number of hat controls
##print "No. of hat controls: ", j.get_numhats()
##
###Get and print number of axes
##print "No. of axes: ", j.get_numaxes()

print "STARTING SERVER ON LOCALHOST"
# try:
address=raw_input("Host:Port (localhost:8000): ")
if not address:
    host, port="localhost", 8000
else:
    host,port=address.split(":")
boxesServe = BoxesServer(localaddr=(host, int(port)))
while True:
    boxesServe.tick()
    sleep(0.01)
