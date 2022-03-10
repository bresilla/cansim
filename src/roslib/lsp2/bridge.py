import can
import cantools
import os
import roslibpy
import sys
import time

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.clock import Clock

clock = 0.5
quality = 0
capacity = 0
emergency = False
cameras = True


client = roslibpy.Ros(host=sys.argv[1], port=int(sys.argv[2]))
while not client.is_connected:
    try:
        client.run()
    except:
        time.sleep(5)
        print("NOT CONNECTED")

if os.name == 'nt':
    bus = can.interface.Bus(channel=3, bustype='vector', app_name="CANoe")
else:
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

dbc = """VERSION ""
BO_ 2365475321 GBSD: 8 Vector__XXX
  SG_ GroundBasedMachineSpeed : 0|16@1+ (0.001,0) [0|64.255] "m/s" Vector__XXX
BO_ 2314732030 GNSSPositionRapidUpdate: 8 Bridge
  SG_ Longitude : 32|32@1- (1E-007,0) [-180|180] "deg" Vector__XXX
  SG_ Latitude : 0|32@1- (1E-007,0) [-90|90] "deg" Vector__XXX
"""

gbsd = cantools.db.load_string(dbc, 'dbc').get_message_by_name("GBSD")
gnss = cantools.db.load_string(dbc, 'dbc').get_message_by_name("GNSSPositionRapidUpdate")

longitude_topic = roslibpy.Topic(client, '/lsp2/longitude', 'std_msgs/Float32')
latitude_topic = roslibpy.Topic(client, '/lsp2/latitude', 'std_msgs/Float32')
speed_topic = roslibpy.Topic(client, '/lsp2/speed', 'std_msgs/Float32')
odometry_topic = roslibpy.Topic(client, '/lsp2/odometry', 'nav_msgs/Odometry')


def send2can(message):
    try:
        bus.send(message)
        print(message)
    except can.CanError:
        print("Message NOT sent")


def recv4can(db):
    data = None
    try:
        message = bus.recv()
        data = db.decode(message.data)
    except can.CanError:
        print("Message NOT sent")
    return data


def send2topic(topic, message):
    topic.publish(roslibpy.Message(message))
    print(message)


def callback():
    gnss_message = recv4can(gnss)
    gbsd_message = recv4can(gbsd)

    print("BRIDGE:")
    send2topic(speed_topic, {'data': float(gbsd_message["GroundBasedMachineSpeed"])})
    send2topic(longitude_topic, {'data': float(gnss_message["Longitude"])})
    send2topic(latitude_topic, {'data': float(gnss_message["Latitude"])})
    send2topic(odometry_topic, {
        "pose": {
            "pose": {
                "position": {"x": float(gnss_message["Longitude"]), "y": float(gnss_message["Latitude"])}
            }
        },
        "header": {"frame_id": "odom"}
    })
    print("-------\n")

if __name__ == "__main__":
    while True:
        callback()
        time.sleep(0.01)
