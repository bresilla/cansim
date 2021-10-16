import can
import cantools

db = cantools.db.load_file('/home/bresilla/data/code/WUR/r4c/cansim/data/sample.dbc')
bus = can.interface.Bus(channel='vcan1', bustype='socketcan', bitrate=250000)

EEC_MSG = db.get_message_by_name("EEC1")
EEC_MSG_DATA = EEC_MSG.encode({'EngineSpeed':4560})
CCVS_MSG = db.get_message_by_name("CCVS1")
CCVS_MSG_DATA = CCVS_MSG.encode({'WheelBasedVehicleSpeed':110})

print(EEC_MSG)
print(CCVS_MSG)
print(db)

rpm_msg = can.Message(arbitration_id=EEC_MSG.frame_id, data=EEC_MSG_DATA, is_extended_id=True)
kmh_msg = can.Message(arbitration_id=CCVS_MSG.frame_id, data=CCVS_MSG_DATA, is_extended_id=True)

try:
    bus.send(rpm_msg)
    bus.send(kmh_msg)
    print("Message setn on {}".format(bus.channel_info))
except can.CanError:
    print("Message NOT sent")
