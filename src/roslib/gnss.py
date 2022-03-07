import can
import cantools
import time


bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

dbc = """VERSION ""
BO_ 2365194522 PD_Loader: 8 SEND
  SG_ Quality : 0|32@1+ (1,0) [0|100] "%"  Loader
  SG_ Capacity : 32|32@1+ (1,0) [0|4294967295] "mm2/s"  Loader
BO_ 2566834709 DM1: 8 SEND
  SG_ FlashRedStopLamp : 12|2@1+ (1,0) [0|3] "" Vector__XXX
  SG_ FlashAmberWarningLamp : 10|2@1+ (1,0) [0|3] "" Vector__XXX
BO_ 2365475321 GBSD: 8 Vector__XXX
 SG_ GroundBasedMachineSpeed : 0|16@1+ (0.001,0) [0|64.255] "m/s" Vector__XXX
BO_ 2314732030 GNSSPositionRapidUpdate: 8 Bridge
 SG_ Longitude : 32|32@1- (1E-007,0) [-180|180] "deg" Vector__XXX
 SG_ Latitude : 0|32@1- (1E-007,0) [-90|90] "deg" Vector__XXX
"""


dm1 = cantools.db.load_string(dbc, 'dbc').get_message_by_name("DM1")
pdl = cantools.db.load_string(dbc, 'dbc').get_message_by_name("PD_Loader")
gbsd = cantools.db.load_string(dbc, 'dbc').get_message_by_name("GBSD")
gnss = cantools.db.load_string(dbc, 'dbc').get_message_by_name("GNSSPositionRapidUpdate")


def send2can(message):
    try:
        bus.send(message)
        print(message)
    except can.CanError:
        print("Message NOT sent")


while True:
    send2can(can.Message(arbitration_id=gnss.frame_id, data=gnss.encode({'Longitude': 12.6, 'Latitude': 6.5})))
    send2can(can.Message(arbitration_id=gbsd.frame_id, data=gbsd.encode({'GroundBasedMachineSpeed': 61.6})))
    time.sleep(0.1)
