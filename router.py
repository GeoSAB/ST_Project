#import XBee
from time import sleep
from digi.xbee.devices import *
import hashlib
import os

hashData=""
contentGlobal = ""
device = XBeeDevice("/dev/ttyUSB0", 9600)
device.open()

def checkForTransmissions(_message = None, _resp= None):
    print("checking trans")
    global contentGlobal
    if _message:
        content = _message.data
        print("new message TRANS")
        content = content.decode()
        if not content[0:3] == "ms:" :
            return False
        contentGlobal = content
        hashedData = MD5hashData(content[3:]).hexdigest()
        try:
            sendData("hs:"+hashedData,_message.remote_device)
            print("hash sent")
        except:
            print("couldn't send hash to END_DEVICE")
            return False
        
    response = _resp
    if response :
        print("AAAAAAAAAAAAAAAAA")
        responseContent = response.data
        responseContent =responseContent.decode()
        print("RESP: ",responseContent)
        if responseContent == "an:ok" :
            contentGlobal = ""
            storeData(contentGlobal)
            return True
        else :
            print("NOPE TRANS")
            return False
    else : return False

def checkForCoordinator(_message=None, _resp = None):
    global hashData
    if _message:
        content = _message.data
        print("new message COORD")
        content = content.decode()
        print("FSFDSFSF",content)
        if(content == "co:") :
            dataToSend = ""
            file = open("data.txt","r")
            for line in file.readlines() :
                dataToSend = dataToSend + line
            
            hashData = hashlib.md5(dataToSend.encode()).hexdigest()
            
            try :
                sendData(dataToSend,Msg.remote_device)
            except :
                print("CANT SEND DATA TO COORD")
                return

            #response = device.read_data(1000)
    response = _resp
    if response :
        responseContent = response.data
        responseContent =responseContent.decode()
        print("resp coord",responseContent, "mine",hashData)
        
        if responseContent[0:3] == "hs:" and responseContent[3:] == hashData :
            sendData("an:ok", Msg.remote_device)
            hashData = ""
            print("data sent")
            os.remove("data.txt")
        else :
            print("NOPE COORD")

            

def MD5hashData(data) : 
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
    file = open("data.txt","a")
    file.writelines(data)
    file.close()

while 1 :
    broadcastPresence()  
    Msg = device.read_data()
    if Msg:
        content = Msg.data
       
        content = content.decode()
        print("new message READ",content)
        if content[0:3] == "ms:" :
            checkForTransmissions(_message=Msg)
        elif content == "an:ok" :
            checkForTransmissions(_resp=Msg)
        elif content[0:3] == "co:" :
            if os.path.exists("data.txt") :
                checkForCoordinator(_message=Msg)
                print("")
        elif content[0:3] == "hs:" :
            if os.path.exists("data.txt") :
                checkForCoordinator(_resp=Msg)
    #checkCoordinator()
   # sleep(0.2)