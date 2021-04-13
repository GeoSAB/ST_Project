import XBee
from time import sleep
from digi.xbee.devices import *
import hashlib
import os


device = XBeeDevice("/dev/ttyUSB1", 9600)
device.open()

def checkForTransmissions():
    Msg = device.read_data(100000)
    if Msg:
        content = Msg.data
        print("new message")
        content = content.decode()
        if not content[:2] == "ms:"
            return False

        hashedData = hasData(content).hexdigest()
        
        sendData(hashedData,Msg.remote_device)
        
        response = device.read_data(100000)
        if not response.remote_device == Msg.remote_device :
            while not response.remote_device == Msg.remote_device :
                response = device.read_data(100000)
        
        if response :
            responseContent = response.data
            responseContent =responseContent.decode()
            if responseContent == "an:ok" :
                storeData(content)
                return True
            else :
                print("NOPE")
                return False
    else : return False

def checkForCoordinator():
    Msg = device.read_data(100000)
    if Msg:
        content = Msg.data
        print("new message")
        content = content.decode()
        if(content == "coordinator") :
            dataToSend = ""
            file = open("file.txt",r)
            for line in file.readlines :
                dataToSend = dataToSend + line
            
            hashData = hashlib.md5(dataToSend)
            
            sendData(dataToSend,Msg.remote_device)

            response = device.read_data(100000)

            if response :
                responseContent = response.data
                responseContent =responseContent.decode()
                if responseContent == hashData :
                    sendData("data_ok", Msg.remote_device)
                    print("data sent")
                    os.remove("data.txt")
                else :
                    print("NOPE")

            

def hashData(data) : 
    return hashlib.md5(data)

def sendData(data,remote_device):
    device.send_data(remote_device,data)

def broadcastPresence() :
    device.send_data_broadcast("router")

def storeData(data):
    file = open("data.txt")
    file.write(data)
    file.close()

while 1 :
    broadcastPresence()
    isData = checkForTransmissions()
    if isData :
        checkForCoordinator()
    sleep(0.5)