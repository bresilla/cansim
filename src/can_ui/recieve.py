import can
import cantools
import os

db = cantools.db.load_file('/home/bresilla/data/code/WUR/r4c/cansim/data/sample.dbc')
if os.name == 'nt':
    #bus = can.interface.Bus(channel='PCAN_USBBUS1', bustype='pcan', bitrate=250000, fd=True)
    bus = can.interface.Bus(channel=0, bustype='vector', bitrate=250000, fd=True)
else:
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan', bitrate=250000, fd=True)




clock = 0.01
quality = 0
capacity = 0


# while True:
#     message = bus.recv()
#     message_decoded = db.decode_message(message.arbitration_id, message.data)
#     print(message_decoded)
#     if 'AreaPerTimeCapacity' in message_decoded:
#         capacity = message_decoded['AreaPerTimeCapacity']
#     print(capacity)

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang.builder import Builder
from kivy.clock import Clock

Builder.load_file("/home/bresilla/data/code/WUR/r4c/cansim/src/ui.kv")
class MyLayout(Widget):
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        Clock.schedule_interval(self.callback, 0.1)

    def slide_capacity(self, *args):
        global capacity
        capacity = int(args[1])
        self.capacity_slider_value.text = str(capacity)
        self.capacity_progress.value = int(capacity)

    def slide_quality(self, *args):
        global quality
        quality = int(args[1])
        self.quality_slider_value.text = str(quality)

    def callback(self, dt):
        message = bus.recv()
        message_decoded = db.decode_message(message.arbitration_id, message.data)
        if 'AreaPerTimeCapacity' in message_decoded:
            self.capacity_progress.value = int(message_decoded['AreaPerTimeCapacity'])


class MyApp(App):
    def build(self):
        return MyLayout()

def callback(dt, app):
    # message = bus.recv()
    # message_decoded = db.decode_message(message.arbitration_id, message.data)
    # print(message_decoded)
    # if 'AreaPerTimeCapacity' in message_decoded:
    #     capacity = message_decoded['AreaPerTimeCapacity']
    # print(capacity)
    pass

if __name__ == "__main__":
    MyApp().run()
