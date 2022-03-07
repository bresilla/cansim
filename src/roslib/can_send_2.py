import can
import cantools
import roslibpy

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.clock import Clock

clock = 0.5
quality = 0
capacity = 0
emergency = False
cameras = True


class Runner():
    def __init__(self):
        self.canbus = None
        self.rosbridge = None
        self.quality = 0
        self.capacity = 0
        self.emergency = False
        self.cameras = True
        self.dbc = """VERSION ""
        BO_ 2365194522 PD_Loader: 8 SEND
            SG_ Quality : 0|32@1+ (1,0) [0|100] "%"  Loader
            SG_ Capacity : 32|32@1+ (1,0) [0|4294967295] "mm2/s"  Loader
        BO_ 2566834709 DM1: 8 SEND
            SG_ FlashRedStopLamp : 12|2@1+ (1,0) [0|3] "" Vector__XXX
            SG_ FlashAmberWarningLamp : 10|2@1+ (1,0) [0|3] "" Vector__XXX
        """
        self.dm1 = cantools.db.load_string(dbc, 'dbc').get_message_by_name("DM1")
        self.pdl = cantools.db.load_string(dbc, 'dbc').get_message_by_name("PD_Loader")
        self.amber_topic = roslibpy.Topic(client, '/lsp1/camera_on_flag', 'std_msgs/Bool')
        self.red_topic = roslibpy.Topic(client, '/lsp1/emergency_stop_flag', 'std_msgs/Bool')
        self.capacity_topic = roslibpy.Topic(client, '/lsp1/capacity', 'std_msgs/Int16')
        self.quality_topic = roslibpy.Topic(client, '/lsp1/quality', 'std_msgs/Int16')

    def send2can(self, message):
        try:
            self.canbus.send(message)
            print(message)
        except can.CanError:
            print("Message NOT sent")

    def send2topic(self, topic, message):
        topic.publish(roslibpy.Message({'data': message}))
        print(message)


def callback(dt, runner):
    print("CAN:")
    runner.send2can(can.Message(
        arbitration_id=runner.pdl.frame_id,
        data=pdl.encode({'Capacity': runner.capacity, 'Quality': runner.quality})))
    runner.send2can(can.Message(
        arbitration_id=runner.dm1.frame_id,
        data=runner.dm1.encode({'FlashAmberWarningLamp': int(runner.cameras), 'FlashRedStopLamp': int(runner.emergency)})))
    print("BRIDGE:")
    runner.send2topic(runner.capacity_topic, capacity)
    runner.send2topic(runner.quality_topic, quality)
    runner.send2topic(runner.amber_topic, cameras)
    runner.send2topic(runner.red_topic, emergency)
    print("-------\n")


Builder.load_file("src/roslib/control.kv")


class MyLayout(Widget):
    def __init__(self, runner, *args, **kwargs):
        self.runner = runner

    def slide_capacity(self, *args):
        self.runner.capacity = int(args[1])
        self.capacity_slider_value.text = str(self.runner.capacity)
        # send2topic(capacity_topic, capacity)
        # send2can(can.Message(arbitration_id=capacity_msg.frame_id, data=capacity_msg.encode({'Capacity':capacity})))

    def slide_quality(self, *args):
        self.runner.quality = int(args[1])
        self.quality_slider_value.text = str(quality)
        # send2topic(quality_topic, quality)
        # send2can(can.Message(arbitration_id=quality_msg.frame_id, data=quality_msg.encode({'Quality':quality})))

    def switch_cameras(self, switchObject, switchValue):
        self.runner.cameras = bool(switchValue)
        # send2topic(amber_topic, cameras)
        # send2can(can.Message(arbitration_id=amber_msg.frame_id, data=amber_msg.encode({'FlashAmberWarningLamp':int(cameras)})))

    def button_emergency(self):
        self.runner.emergency = not emergency
        # send2topic(red_topic, emergency)
        # send2can(can.Message(arbitration_id=red_msg.frame_id, data=red_msg.encode({'FlashRedStopLamp':int(emergency)})))


class MyApp(App):
    def build(self):
        return MyLayout()


if __name__ == "__main__":
    Clock.schedule_interval(callback, clock)
    MyApp().run()
