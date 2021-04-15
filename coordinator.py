import hashlib
from datetime import datetime
from time import sleep
from pathlib import Path
from digi.xbee.devices import *

message = ""
data = []
data_test = []

remote_device =  None
current_data = "" #store the data while it's being check to see if it's ok



#def receive_data(rm_device):

    
def generate_hash(str):
    return hashlib.md5(str.encode())

def answer(Msg, remote_device):
    content = Msg.data
    content = content.decode()
    print(content)
    #device.send_data(remote_device, content)

def generate_answer(Msg, coor):
    global message
    global remote_device
    data_msg = (Msg.data).decode()
    remote_device = "test"
    bstr = ""
    hash = ""

    if(remote_device): #to be addressed later
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
                st += hash.hexdigest()
                print(st)
                coor.send_data(Msg.remote_device, st)
                print("hash sent")
                message = msg
            except:
                print("Error while sending the hash")

        elif (bstr == "an:"):
            print(bstr)
            print(msg)
            if(msg == "ok" and message):
                now = datetime.now()
                f = open("coor.txt", "a")
                f.write(now.strftime("%m/%d/%Y, %H:%M:%S") + " |\n" + message + "\n")
                message = ""
            else :
                print("error the data hasn't been received correctly")
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

    while(True):

        try:
            coordinator_device.send_data_broadcast("co:")
            print("Broadcast")
        except:
            d = datetime.now()
            print("could not broadcast " + d.strftime("%m/%d/%Y, %H:%M:%S"))
        
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
    




    
    
