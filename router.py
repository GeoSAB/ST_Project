#import XBee
from time import sleep
from digi.xbee.devices import *
import hashlib
import os

hashData=""
contentGlobal = ""
device = XBeeDevice("/dev/ttyUSB1", 9600)
device.open()
remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string("0013A20041C6287E"))

messageList=[]
messageListE_D=[]

class MessageCheck:
    def __init__(self,message,hashDigest):
        self.message = message
        self.hashDigest = hashDigest

def inMessageListE_D(p):
    for i in range(0, len(messageListE_D)):
        print("inmsg", messageListE_D[i].hashDigest)
        if p == messageListE_D[i].hashDigest:
            return i
    return -1

def isHashInSentList(hs):
    global messageList
    for message in messageList :
        if (message.hashDigest == hs):
            messageList.remove(message)
            return True
    return False

def checkForTransmissions(_message = None, _resp= None):
    print("checking trans")
    global contentGlobal
    if _message:
        content = _message.data
        print("new message TRANS")
        content = content.decode()
        if not content[0:3] == "ms:" :
            return False
        hashedData = MD5hashData(content[3:]).hexdigest()
        c = MessageCheck(content[3:],hashedData)
        messageListE_D.append(c)
        try:
            sendData("hs:"+hashedData,_message.remote_device)
            print("hash sent")
        except:
            print("couldn't send hash to END_DEVICE")
            return False
        
    response = _resp
    if response :
        responseContent = response.data
        responseContent =responseContent.decode()
        print("RESP: ",responseContent[3:])
        if responseContent == "an:nk" :

            print("NOPE TRANS")
            return False

        else :
            ind = inMessageListE_D(responseContent[3:])
            if ind >= 0 :
                storeData(messageListE_D[ind].message)
                messageListE_D.pop(ind)
                return True
            else :
                print("error not in the message list")
                return False

    else : return False

def checkForCoordinator(_message=None, _resp = None):
    global hashData,messageList
    if _message:
        content = _message.data
        #print("new message COORD")
        content = content.decode()
        #print("FSFDSFSF",content)
        if(content == "co:") :
            dataToSend = ""
            file = open("data.txt","r")
            dataToSend = "ms:"
            for line in file.readlines() :
                dataToSend = dataToSend + line
            
            hashData = hashlib.md5(dataToSend.encode()).hexdigest()
            
            try :
                sendData(dataToSend,Msg.remote_device)
                m = MessageCheck(dataToSend,hashData)
                messageList.append(m)
            except :
                print("CANT SEND DATA TO COORD",Msg.remote_device)
                return

            #response = device.read_data(1000)
    response = _resp
    if response :
        responseContent = response.data
        responseContent =responseContent.decode()
        print("recieved hash from coord",responseContent, "mine",hashData)
        
        if responseContent[0:3] == "hs:" :
            if(isHashInSentList(responseContent[3:])):
                sendData(("an:"+responseContent[3:]), Msg.remote_device)
                hashData = ""
                print("data sent")
                os.remove("data.txt")
        else :
            print("hash from coord is incorrect")

            

def MD5hashData(data) : 
    return hashlib.md5(data.encode())

def sendData(data,remote_device):
    device.send_data(remote_device,data)

def broadcastPresence() :
    try :
        #print("router")
        device.send_data(remote_device,"rq:")
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
        print("new message, content:",content)
        if content[0:3] == "ms:" :
            checkForTransmissions(_message=Msg)
        elif content[0:3] == "an:" and len(content) > 5:
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