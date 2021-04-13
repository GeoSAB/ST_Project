import XBee
from time import sleep
from digi.xbee.devices import *
import hashlib

data_to_send = ""
data_hash = ""
num_of_line = 0

def read_sensor_data(line_num):
    with open("data.txt") as file:
        content = file.readlines()
    return content[num_of_line]


def generate_answer(Msg):

    data = Msg.data.decode()
    remote_device = Msg.remote_device

    if (remote_device == drone_id):
        #treat message

        if (data == "Request"):
            global data_to_send = read_sensor_data(num_of_line)
            global data_hash = hashlib.md5(data_to_send).hexdigest()

            return remote_device, read_sensor_data(num_of_line)

        elif (data.hexdigest() == data_hash):
            return remote_device, "OK"

        else:
            return remote_device, "NOT OK"

    else:
        return null, null



def main():

    device = XBeeDevice("/dev/ttyUSB1", 9600)
    device.open()

    while(1):  #while loop representing sleep state
        
        Msg = device.read_data(100000)

        if Msg:    
            remote_device, data = generate_answer(Msg)
            device.send_data(remote_device, data)


if __name__ == "__main__":
    main()

