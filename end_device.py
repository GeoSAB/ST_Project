import XBee
from time import sleep
from digi.xbee.devices import *
import hashlib

data_to_send = ""
data_hash = ""
num_of_line = 0
drone_id = "key"

def read_sensor_data(line_num):
    with open("data.txt") as file:
        content = file.readlines()
    return content[num_of_line]


def generate_answer(Msg):

    #data = Msg.data.decode()
    data = "rq:hello"
    #remote_device = Msg.remote_device
    remote_device = "key"
    global num_of_line

    if (remote_device == drone_id):
        #treat message

        code = data[0:2]

        if (code == "rq"):
            global data_to_send 
            data_to_send = read_sensor_data(num_of_line).encode()
            global data_hash 
            data_hash = hashlib.md5(data_to_send).hexdigest()

            return remote_device, read_sensor_data(num_of_line)

        elif (code == "hs"):
            if (data[2:].hexdigest() == data_hash):
                num_of_line += 1
                return remote_device, "an:ok"

            else:
                num_of_line -= 1
                return remote_device, "an:nk"
        else:
            remote_device, "an:unknown"

    else:
        return null, null



def main():

    #device = XBeeDevice("/dev/ttyUSB1", 9600)
    #device.open()

    while(1):  #while loop representing sleep state
        
        #Msg = device.read_data(100000)
        Msg = "hs:requesting data"

        if Msg:    
            remote_device, data = generate_answer(Msg)
            #device.send_data(remote_device, data)
            print(remote_device, data)


if __name__ == "__main__":
    main()

