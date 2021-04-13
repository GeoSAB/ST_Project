import XBee
import hashlib
from time import sleep
from digi.xbee.devices import *


def receive_data()
def generate_hash(str):




if __name__ == "__main__":
    #device = XBeeDevice("/dev/tty.usbserial-A50285BI", 9600)
    #device.open()
    router_msg = "hello this is a message from tthe router"

    if router_msg:
        
        

    print("ready to send")
    # Send broadcast data.
    device.send_data_broadcast("hello:0013A20041C5FE13")

    #remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string("0013A20041C6287E"))

    # A simple string message
    
    def answer(Msg, remote_device):
        content = Msg.data
        content = content.decode()
        print(content)
        device.send_data(remote_device, content)

    while(True):
        try:
            Msg = device.read_data(100)
            if Msg :
                answer(Msg, Msg.remote_device)
        except ValueError:
            print("error while reading")




    
    
