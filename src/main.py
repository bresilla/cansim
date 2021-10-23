import can
import cantools

db = cantools.db.load_file('/home/bresilla/data/code/WUR/r4c/cansim/data/sample.dbc')
bus = can.interface.Bus(channel='vcan0', bustype='socketcan', bitrate=250000, fd=True)

quality = 0
capacity = 0

PD_TC = db.get_message_by_name("PD_TC")
EEC_MSG = db.get_message_by_name("EEC1")


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang.builder import Builder
from kivy.clock import Clock

Builder.load_file("/home/bresilla/data/code/WUR/r4c/cansim/src/ui.kv")

def callback(dt):
    capacity_message = can.Message(arbitration_id=PD_TC.frame_id, data=PD_TC.encode({'AreaPerTimeCapacity':capacity}), is_fd=True)
    quality_message = can.Message(arbitration_id=EEC_MSG.frame_id, data=EEC_MSG.encode({'EngineSpeed':quality}), is_fd=True)

    try:
        bus.send(capacity_message)
        bus.send(quality_message)
        print(capacity_message)
        print(quality_message)
    except can.CanError:
        print("Message NOT sent")


class MyLayout(Widget):
    def slide_capacity(self, *args):
        self.capacity_slider_value.text = str(int(args[1]))
        global capacity
        capacity = int(args[1])
        capacity_encoded = PD_TC.encode({'AreaPerTimeCapacity':capacity})
        capacity_message = can.Message(arbitration_id=PD_TC.frame_id, data=capacity_encoded, is_fd=True)
        try:
            bus.send(capacity_message)
            print("Message {} set on {}".format(args[1], bus.channel_info))
        except can.CanError:
            print("Message NOT sent")

    def slide_quality(self, *args):
        self.quality_slider_value.text = str(int(args[1]))
        global quality
        quality = int(args[1])
        quality_encoded = EEC_MSG.encode({'EngineSpeed':quality})
        quality_message = can.Message(arbitration_id=EEC_MSG.frame_id, data=quality_encoded, is_fd=True)

        try:
            bus.send(quality_message)
            print("Message {} set on {}".format(args[1], bus.channel_info))
        except can.CanError:
            print("Message NOT sent")


class MyApp(App):
    def build(self):
        return MyLayout()

if __name__ == "__main__":
    Clock.schedule_interval(callback, 0.5)
    MyApp().run()
