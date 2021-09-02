import socket
import serial
import sys

#=====================================

def sendToArduino(sendStr):
  ser.write(sendStr) #serially send data to Arduino


#======================================

def recvFromArduino():
  global startMarker, endMarker
  
  ck = ""
  x = "z" # any value that is not an end- or startMarker
  byteCount = -1 # to allow for the fact that the last increment will be one too many
  
  # wait for the start character
  while  ord(x) != startMarker: 
    x = ser.read()
  
  # save data until the end marker is found
  while ord(x) != endMarker:
    if ord(x) != startMarker:
      ck = ck + x 
      byteCount += 1
    x = ser.read()
  
  return(ck) #string containing received data


#============================

def waitForArduino():

   # wait until the Arduino sends 'Arduino Ready' - allows time for Arduino reset
   # it also ensures that any bytes left over from a previous message are discarded
   
    global startMarker, endMarker
    
    msg = ""
    while msg.find("Arduino is ready") == -1:

      while ser.inWaiting() == 0:
        pass
        
      msg = recvFromArduino()

      print msg
      print
      
#======================================

def runTest(td):
  numLoops = len(td)
  waitingForReply = False

  n = 0
  while n < numLoops:

    teststr = td[n]

    if waitingForReply == False:
      sendToArduino(teststr)
      print "Sent from PC -- LOOP NUM: " + str(n) + " TEST STR: " + teststr
      waitingForReply = True

    if waitingForReply == True:

      while ser.inWaiting() == 0:
        pass
        
      dataRecvd = recvFromArduino()
      print "Reply Received:  " + dataRecvd
      n += 1
      waitingForReply = False

      print "==========="

##    time.sleep(5)

##Serial connection to Arduino set-up
serPort = "/dev/ttyACM0" #Port address of Arduino on the Pi
baudRate = 9600  #Set data transfer rate
ser = serial.Serial(serPort, baudRate)
print "Serial port " + serPort + " opened  Baudrate " + str(baudRate)


startMarker = 60 #'<'
endMarker = 62 #'>'
waitForArduino() #Wait for arduino to reset and acknowledge connection to PC


##Socket connection to PC
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ('192.168.137.2',21000)
s.bind(address) #Set up connection point for PC

s.listen(1)
while True:
    print 'waiting for a connection'
    conn, addr = s.accept() #Accept connection request from PC
    try:
        print('Connection from ', addr)
        while True:
            data = conn.recv(1024)
            print('Received ', data)
            if data:
                print 'Sending data back'
                conn.sendall(data)
                testData = []
                testData.append(data)
                runTest(testData) #send data to arduino
            else:
                print 'No more data'
                break
    finally:
        conn.close()
