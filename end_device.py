#import XBee
from time import sleep
from digi.xbee.devices import *
import hashlib

class MessageCheck:
    def __init__(self,message,hashDigest):
        self.message = message
        self.hashDigest = hashDigest




messageList = []

data_to_send = ""
data_hash = ""
num_of_line = 0
drone_id = "0013A20041C60D23"

def isHashInSentList(hs):
    global messageList
    for message in messageList :
        if (message.hashDigest == hs):
            messageList.remove(message)
            return True
    return False
    

def read_sensor_data(line_num):
    with open("read.txt") as file:
        content = file.readlines()
    return content[num_of_line]


def generate_answer(Msg):

    data = Msg.data.decode()
    remote_device = Msg.remote_device
    global num_of_line

    code = data[0:2]
    print(str(remote_device)[0:16])

    if (str(remote_device)[0:16] == drone_id):

        print("success id")
        #treat message

        if (code == "rq"):
            global data_to_send 
            data_to_send = read_sensor_data(num_of_line)
            global data_hash 
            data_hash = hashlib.md5(data_to_send.encode()).hexdigest()
            data_to_send = "ms:" + data_to_send

            print("sending data: ", data_to_send)

            return remote_device, data_to_send , data_hash

        elif (code == "hs"):
            print("received hash:", data[3:], data_hash)
            if (isHashInSentList(data[3:])):
                num_of_line += 1
                return remote_device, "an:ok",data_hash

            else:
              
                return remote_device, "an:nk",data_hash
        else:
            remote_device, "an:unknown", 0

    else:
        return 0, 0, 0



def main():
    global messageList
    device = XBeeDevice("/dev/ttyUSB0", 9600)
    device.open()

    while(1):  #while loop representing sleep state
        
        print("waiting for message")
        msg = device.read_data(100)
        print("message ", (msg.data).decode())

        if msg:    
            remote_device, data ,hash_data = generate_answer(msg)
            if (remote_device != 0):
                m = MessageCheck(data,hash_data)
                messageList.append(m)
                device.send_data(remote_device, data)
            print(remote_device, data)


if __name__ == "__main__":
    main()