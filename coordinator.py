import hashlib
from datetime import datetime
from time import sleep
from pathlib import Path
from digi.xbee.devices import *
import time

data = []
data_test = []

remote_device =  None
current_data = "" #store the data while it's being check to see if it's ok

c = False
messageList = []


#def receive_data(rm_device):

class MessageCheck:
    def __init__(self,message,hashDigest):
        self.message = message
        self.hashDigest = hashDigest

def inMessageList(p):
    for i in range(0, len(messageList)):
        print("inmsg", messageList[i].hashDigest)
        if p == messageList[i].hashDigest:
            return i
    return -1

    
def generate_hash(str):
    return hashlib.md5(str.encode())

def answer(Msg, remote_device):
    content = Msg.data
    content = content.decode()
    print(content)
    #device.send_data(remote_device, content)

def generate_answer(Msg, coor):
    global c
    global remote_device
    data_msg = (Msg.data).decode()
    bstr = ""
    hash = ""

    if(Msg.remote_device): #to be addressed later
        bstr = data_msg[0:3]
        msg = data_msg[3:]
        if(bstr == "ms:"):
            print(bstr)
            print(msg)
            print("received data")
            hash = generate_hash(data_msg)
            try:
                print(Msg.remote_device)
                print(hash.hexdigest())
                st = "hs:"
                st += str(hash.hexdigest())
                print(st)
                coor.send_data(Msg.remote_device, st)
                m = MessageCheck(msg, hash.hexdigest())
                messageList.append(m)
                print("sent")
            except:
                print("Error while sending the hash")

        elif (bstr == "an:"):
            print(bstr)
            print(msg)
            if msg == "nk":
                print("error the data hasn't been received correctly by the router")
            else :
                ind = inMessageList(msg)
                if ind >= 0:
                    now = datetime.now()
                    f = open("coor.txt", "a")
                    f.write(now.strftime("%m/%d/%Y, %H:%M:%S") + " |\n" + messageList[ind].message + "\n")
                    messageList.pop(ind)
        
        elif (bstr == "rq:"):
            pass
        else:
            print("unrecognized msg")
    else:
        print("error id")    


def main():

    coordinator_device = XBeeDevice("/dev/tty.usbserial-A50285BI", 9600)
    coordinator_device.open()
    router_msg = None
    base_t = time.time()
    nb_b = 0
    b = False
    while(True):
        t = time.time()
        if t > base_t + 15 or nb_b == 0: 
            try:
                    coordinator_device.send_data_broadcast("co:")
                    nb_b = 1
                    b = True
                    d = datetime.now()
                    print("Broadcast " + d.strftime("%m/%d/%Y, %H:%M:%S"))
            except:
                d = datetime.now()
                print("could not broadcast " + d.strftime("%m/%d/%Y, %H:%M:%S"))
        if b :
            base_t = time.time()
            b = False
        
        try:
            router_msg = coordinator_device.read_data()
        except:
            d = datetime.now()
            print("could not read data " + d.strftime("%m/%d/%Y, %H:%M:%S"))

        if router_msg:
            generate_answer(router_msg, coordinator_device)
            

        # Send broadcast data.
        #device.send_data_broadcast("hello:0013A20041C5FE13")

        #remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string("0013A20041C6287E"))

        # A simple string message




if __name__ == "__main__":
    main()
    




    
    
