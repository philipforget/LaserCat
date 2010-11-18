import os
import sys
import time
import threading

import OSC # simpleosc
import serial # pyserial

COM_PORT = '/dev/ttyACM0' # set this to the serial port to which the Make Controller is connected, something like "COM0" for windows or "/dev/ttyACM0" for POSIX
SLIP_END = '\xC0' #end of an OSC message with SLIP wrapping (USB only)
SLIP_ESC = '\xDB' # used to escape embedded OSC messages

class Lm34Read(object):

    def __init__(self, comPortId):
        self._initializeSerial(comPortId)
        self._inBuffer = ''

    def _initializeSerial(self, comPortId):
        self._serial = serial.Serial(comPortId, 115200, timeout = 0)  # open the virtual serial port created by the Make Controller's USB interface

    def _write(self, address, value = None):
        m = OSC.OSCMessage() #create a new OSC messsage
        m.setAddress(address) #set the address to the one specified by the parameter

        if value is not None: # if we are passing a param along with the address...
            m.append(value)

        s = str(m).replace(SLIP_END, SLIP_ESC + SLIP_END) # escape any embedded SLIP_END characters in the message
        self._serial.write(SLIP_END + s + SLIP_END) # begin and end with SLIP_END; doesn't seem to work otherwise

    def _read(self):
        print self._serial.read(500);
        return
        if self._serial.inWaiting():
            for c in self._serial.read(500): # read 500 bytes, or as much as is in the buffer
                if c == SLIP_END and (len(self._inBuffer) == 0 or self._inBuffer[-1] != SLIP_ESC): #if the EOM char is in the message, and the buffer is empty or the last buffer char is not an escape character
                    self._handleInput() #process the data
                else: #otherwise
                    self._inBuffer += c # append what was just read to the buffer

    def _handleInput(self):
        message = OSC.decodeOSC(self._inBuffer) #decode the message and make an array of it
        if len(message) != 0: #if the message is present
            print str(message[2]) #print our temperature

        self._inBuffer = '' #wipe the serial buffer

    def run(self):
        #self._write('/appled/0/value', 1 if self.poop else 0) #send a message requesting the value of the zeroth analog input
        self._write('/appled/0/active') #send a message requesting the value of the zeroth analog input
        time.sleep(0.5) #give the Make Controller a chance to poll and respond (value in seconds)
        self._read() # check for any new messages from the Make Controller
        t = threading.Timer(1, self.run).start() #make a new timer to run 1 second after this function finishes execution


if __name__ == "__main__":
    app = Lm34Read(comPortId = COM_PORT)
    t = threading.Timer(1, app.run) #setup a timer to fire after 1.0 second
    t.start() #start the timer
