import can
import cantools

db = cantools.db.load_file('/home/bresilla/data/code/WUR/r4c/cansim/data/sample.dbc')

bus = can.interface.Bus(channel='vcan1', bustype='socketcan', bitrate=250000)
while True:
    message = bus.recv()
    print(db.decode_message(message.arbitration_id, message.data))
