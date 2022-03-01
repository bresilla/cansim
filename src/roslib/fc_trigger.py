import argparse
import roslibpy
import time


class CommandLine:
    def __init__(self):
        parser = argparse.ArgumentParser(description="COMPUTER POWER STATUS")
        parser.add_argument("-t", "--topic", help="topic in which the status is send", required=False, default="/lsp1/computer_on")
        parser.add_argument("-p", "--port", help="port of ROS_BRIDGE server", required=False, default="2233")
        parser.add_argument("-i", "--ip", help="ip of ROS_BRIDGE server", required=False, default="150.140.148.242")

        argument = parser.parse_args()
        status = False

        if argument.topic:
            print("You have used '-t' or '--topic' with argument: {0}".format(argument.topic))
            self.topic = argument.topic
            status = True
        if argument.port:
            print("You have used '-p' or '--port' with argument: {0}".format(argument.port))
            self.port = argument.port
            status = True
        if argument.ip:
            print("You have used '-i' or '--ip' with argument: {0}".format(argument.ip))
            self.ip = argument.ip
            status = True
        if not status:
            print("Maybe you want to use -h, -t, -p or -i as arguments ?")


if __name__ == '__main__':
    app = CommandLine()

    while True:
        client = roslibpy.Ros(host=app.ip, port=int(app.port))
        if client.is_connected:
            client.run()
            talker = roslibpy.Topic(client, app.topic, 'std_msgs/Bool')
            talker.publish(roslibpy.Message({'data': True}))
            time.sleep(1)
            print("Topic send to server...")
        else:
            time.sleep(1)
            print("Not connected to server...")
