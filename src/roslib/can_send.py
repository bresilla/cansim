import can
import cantools
import os
import roslibpy
import sys
import time

client=roslibpy.Ros(host= sys.argv[1], port= int(sys.argv[2]))
client.run()
print(client.is_connected)

if os.name == 'nt':
    #bus = can.interface.Bus(channel='PCAN_USBBUS1', bustype='pcan', bitrate=250000)
    bus = can.interface.Bus(channel=0, bustype='vector', bitrate=500000)
else:
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan', bitrate=500000)


amber_string="""VERSION ""
BO_ 2566834709 DM1: 8 SEND
 SG_ FlashAmberWarningLamp : 10|2@1+ (1,0) [0|3] "" Vector__XXX
"""

red_string="""VERSION ""
BO_ 2566834709 DM1: 8 SEND
 SG_ FlashRedStopLamp : 12|2@1+ (1,0) [0|3] "" Vector__XXX
"""

capacity_string="""VERSION ""
BO_ 2365194522 PD_Loader: 8 SEND
 SG_ Capacity : 32|32@1+ (1,0) [0|4294967295] "mm2/s"  Loader
"""

quality_string="""VERSION ""
BO_ 2365194522 PD_Loader: 8 SEND
 SG_ Quality : 0|32@1+ (1,0) [0|100] "%"  Loader
"""


clock = 0.5
quality = 0
capacity = 0
emergency = False
cameras = True

amber_msg = cantools.db.load_string(amber_string, 'dbc').get_message_by_name("DM1")
red_msg = cantools.db.load_string(red_string, 'dbc').get_message_by_name("DM1")
capacity_msg = cantools.db.load_string(capacity_string, 'dbc').get_message_by_name("PD_Loader")
quality_msg = cantools.db.load_string(quality_string, 'dbc').get_message_by_name("PD_Loader")

amber_topic=roslibpy.Topic(client,'/lsp1/camera_on_flag','std_msgs/Bool')
red_topic=roslibpy.Topic(client,'/lsp1/emergency_stop_flag','std_msgs/Bool')
capacity_topic=roslibpy.Topic(client,'/lsp1/capacity','std_msgs/Int16')
quality_topic=roslibpy.Topic(client,'/lsp1/quality','std_msgs/Int16')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang.builder import Builder
from kivy.clock import Clock


def send2can(message):
    try:
        bus.send(message)
        print(message)
    except can.CanError:
        print("Message NOT sent")

def send2topic(topic, message):
    topic.publish(roslibpy.Message({'data': message}))
    print(message)

def callback(dt):
    print("CAN:")
    send2can(can.Message(arbitration_id=capacity_msg.frame_id, data=capacity_msg.encode({'Capacity':capacity})))
    send2can(can.Message(arbitration_id=quality_msg.frame_id, data=quality_msg.encode({'Quality':quality})))
    send2can(can.Message(arbitration_id=amber_msg.frame_id, data=amber_msg.encode({'FlashAmberWarningLamp':int(cameras)})))
    send2can(can.Message(arbitration_id=red_msg.frame_id, data=red_msg.encode({'FlashRedStopLamp':int(emergency)})))
    print("BRIDGE:")
    send2topic(capacity_topic, capacity)
    send2topic(quality_topic, quality)
    send2topic(amber_topic, cameras)
    send2topic(red_topic, emergency)
    print("-------\n")

Builder.load_file("src/roslib/control.kv")
class MyLayout(Widget):
    def slide_capacity(self, *args):
        global capacity
        capacity = int(args[1])
        self.capacity_slider_value.text = str(capacity)
        #send2topic(capacity_topic, capacity)
        #send2can(can.Message(arbitration_id=capacity_msg.frame_id, data=capacity_msg.encode({'Capacity':capacity})))

    def slide_quality(self, *args):
        global quality
        quality = int(args[1])
        self.quality_slider_value.text = str(quality)
        # send2topic(quality_topic, quality)
        # send2can(can.Message(arbitration_id=quality_msg.frame_id, data=quality_msg.encode({'Quality':quality})))

    def switch_cameras(self, switchObject, switchValue):
        global cameras
        cameras = bool(switchValue)
        # send2topic(amber_topic, cameras)
        # send2can(can.Message(arbitration_id=amber_msg.frame_id, data=amber_msg.encode({'FlashAmberWarningLamp':int(cameras)})))
 
    def button_emergency(self):
        global emergency
        emergency = not emergency
        # send2topic(red_topic, emergency)
        # send2can(can.Message(arbitration_id=red_msg.frame_id, data=red_msg.encode({'FlashRedStopLamp':int(emergency)})))

class MyApp(App):
    def build(self):
        return MyLayout()

if __name__ == "__main__":
    Clock.schedule_interval(callback, clock)
    MyApp().run()
