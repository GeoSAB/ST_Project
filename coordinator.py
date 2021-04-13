import hashlib
from datetime import datetime
from time import sleep
from digi.xbee.devices import *

data = []
data_test = []
s = "hello this is a message from the router"
r_hash = hashlib.md5(s.encode())

remote_device = "test"
router_id = "test"
coordinator_device = ""
current_data = "" #store the data while it's being check to see if it's ok



#def receive_data(rm_device):

    
def generate_hash(str):
    return hashlib.md5(str.encode())

def answer(Msg, remote_device):
    content = Msg.data
    content = content.decode()
    print(content)
    #device.send_data(remote_device, content)

def generate_answer(Msg):
    global remote_device
    global coordinator_device
    data_msg = Msg
    remote_device = "test"
    bstr = ""
    hash = ""

    if(remote_device == router_id): #to be addressed later
        bstr = data_msg[0:3]
        print(bstr)
        msg = data_msg[3:]
        print(msg)
        if(bstr == "ms:"):
            hash = generate_hash(msg)
            if(hash.hexdigest() == r_hash.hexdigest()):
                data_test.append("an:ok")
            else :
                data_test.append("an:nk")
                #coordinator_device.send_data(remote_device, hash)

        elif (bstr == "an:"):
            if(msg == "ok"):
                k = []
                now = datetime.now()
                k.append(now)
                k.append(current_data)
                data.append(k)
            else :
                print("error the data hasn't been received correctly")
        else:
            print("unrecognized msg")
    else:
        print("error id")    


def main():
    #device = XBeeDevice("/dev/tty.usbserial-A50285BI", 9600)
    #device.open()

    router_msg = "ms:hello this is a message from the router"
    data_test.append(router_msg)
    i = 0
    while(i < len(data_test)):
        print("ready")

        #router_msg = device.read_data(100000)

        if router_msg:
            print("got a message")
            generate_answer(data_test[i])

            sleep(2)

        i += 1
            

        # Send broadcast data.
        #device.send_data_broadcast("hello:0013A20041C5FE13")

        #remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string("0013A20041C6287E"))

        # A simple string message




if __name__ == "__main__":
    main()
    




    
    
