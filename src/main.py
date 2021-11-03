import can
import cantools
import os


db = cantools.db.load_file('data/sample.dbc')
if os.name == 'nt':
    bus = can.interface.Bus(channel='PCAN_USBBUS1', bustype='pcan', bitrate=250000, fd=True)
else:
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan', bitrate=250000, fd=True)


clock = 0.5
quality = 0
capacity = 0

PD_TC = db.get_message_by_name("PD_TC")
EEC_MSG = db.get_message_by_name("EEC1")


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

def callback(dt):
    send2can(can.Message(arbitration_id=PD_TC.frame_id, data=PD_TC.encode({'AreaPerTimeCapacity':capacity}), is_fd=True))
    send2can(can.Message(arbitration_id=EEC_MSG.frame_id, data=EEC_MSG.encode({'EngineSpeed':quality}), is_fd=True))

Builder.load_file("src/control.kv")
class MyLayout(Widget):
    def slide_capacity(self, *args):
        global capacity
        capacity = int(args[1])
        self.capacity_slider_value.text = str(capacity)
        send2can(can.Message(arbitration_id=PD_TC.frame_id, data=PD_TC.encode({'AreaPerTimeCapacity':capacity}), is_fd=True))

    def slide_quality(self, *args):
        global quality
        quality = int(args[1])
        self.quality_slider_value.text = str(quality)
        send2can(can.Message(arbitration_id=EEC_MSG.frame_id, data=EEC_MSG.encode({'EngineSpeed':quality}), is_fd=True))

class MyApp(App):
    def build(self):
        return MyLayout()

if __name__ == "__main__":
    Clock.schedule_interval(callback, clock)
    MyApp().run()
