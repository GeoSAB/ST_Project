import XBee
import hashlib
from time import sleep
from digi.xbee.devices import *

data = []


def receive_data(rm_device):
    
    
def generate_hash(str):
    return hashlib.md5(str)

def answer(Msg, remote_device):
    content = Msg.data
    content = content.decode()
    print(content)
    #device.send_data(remote_device, content)


def main():
    #device = XBeeDevice("/dev/tty.usbserial-A50285BI", 9600)
    #device.open()


    while(True):
        hash = "" hs:
                  ms:
                  an:ok
                  an:nk
        router_msg = "ms:hello this is a message from the router"
        if router_msg:

            hash = generate_hash(router_msg)
            answer(hash)
            

        print("ready to send")
        # Send broadcast data.
        #device.send_data_broadcast("hello:0013A20041C5FE13")

        #remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string("0013A20041C6287E"))

        # A simple string message




if __name__ == "__main__":
    main()
    




    
    
