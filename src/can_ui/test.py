import can
import cantools
import time
import os


if os.name == 'nt':
    #bus = can.interface.Bus(channel='PCAN_USBBUS1', bustype='pcan', bitrate=250000, fd=True)
    bus = can.interface.Bus(channel=0, bustype='vector', bitrate=250000, fd=True)
else:
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan', bitrate=500000, fd=True)


db="""VERSION ""
BO_ 2566834709 DM1: 8 SEND
 SG_ FlashAmberWarningLamp : 10|2@1+ (1,0) [0|3] "" Vector__XXX
 SG_ FlashRedStopLamp : 12|2@1+ (1,0) [0|3] "" Vector__XXX

BO_ 2365194522 PD_Loader: 8 SEND
 SG_ Capacity : 32|32@1+ (1,0) [0|4294967295] "mm2/s"  Loader
 SG_ Quality : 0|32@1+ (1,0) [0|100] "%"  Loader
"""

db = cantools.db.load_string(db, 'dbc')

quality = 0
capacity = 0

while True:
    print("------------------------------")
    message = bus.recv()
    message_decoded = db.decode_message(message.arbitration_id, message.data)
    if 'Quality' in message_decoded:
        quality = int(message_decoded['Quality'])

    print(quality)
    time.sleep(0.1)
