#import XBee
from time import sleep
from digi.xbee.devices import *
import hashlib
import os


device = XBeeDevice("/dev/ttyUSB1", 9600)
device.open()

def checkForTransmissions():
    print("checking trans")
    Msg = device.read_data()
    if Msg:
        content = Msg.data
        print("new message TRANS")
        content = content.decode()
        if not content[0:3] == "ms:" :
            print("ERROR transmission")
            return False
        print(content[3:])
        hashedData = hashData(content[3:]).hexdigest()
        print(hashedData)
        try:
            sendData("hs:"+hashedData,Msg.remote_device)
        except:
            print("couldn't send hash to END_DEVICE")
        response = device.read_data(100000)
        if not response.remote_device == Msg.remote_device :
            while not response.remote_device == Msg.remote_device :
                response = device.read_data(100000)
        
        if response :
            responseContent = response.data
            responseContent =responseContent.decode()
            print("RESP: ",responseContent)
            if responseContent == "an:ok" :
                storeData(content)
                return True
            else :
                print("NOPE")
                return False
    else : return False

def checkForCoordinator():
    Msg = device.read_data(1000)
    if Msg:
        content = Msg.data
        print("new message COORD")
        content = content.decode()
        print(content)
        if(content == "co:") :
            dataToSend = ""
            file = open("data.txt","r")
            for line in file.readlines() :
                dataToSend = dataToSend + line
            
            hashData = hashlib.md5(dataToSend.encode())
            
            sendData(dataToSend,Msg.remote_device)

            response = device.read_data(100000)

            if response :
                responseContent = response.data
                responseContent =responseContent.decode()
                print("resp coord",responseContent)
                if responseContent == hashData :
                    sendData("data_ok", Msg.remote_device)
                    print("data sent")
                    os.remove("data.txt")
                else :
                    print("NOPE COORD")

            
def checkCoordinator():
    Msg = device.read_data()
    if Msg:
        content = Msg.data
        print("new message")
        content = content.decode()
        print(content)

def hashData(data) : 
    return hashlib.md5(data.encode())

def sendData(data,remote_device):
    device.send_data(remote_device,data)

def broadcastPresence() :
    try :
        print("router")
        device.send_data_broadcast("rq:")
    except:
        print("Send error")

def storeData(data):
    file = open("data.txt","w")
    file.writelines(data)
    file.close()

while 1 :
    broadcastPresence()
    isData = checkForTransmissions()
    if os.path.exists("data.txt") :
        checkForCoordinator()

    #checkCoordinator()
    sleep(1)