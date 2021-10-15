import can
# import cantools

bus = can.interface.Bus(channel='vcan0', bustype='socketcan', bitrate=250000)
msg = can.Message(arbitration_id=0xc0ffee, data=[0, 25, 0, 1, 3, 1, 4, 1], is_extended_id=False)

try:
    bus.send(msg)
    print("Message setn on {}".format(bus.channel_info))
except can.CanError:
    print("Message NOT sent")
