import roslibpy
import sys
import time

client=roslibpy.Ros(host= sys.argv[1], port= int(sys.argv[2]))
client.run()
print(client.is_connected)
talker=roslibpy.Topic(client,'/triger_flag','std_msgs/Bool')
i=0

if int(sys.argv[3]) == 0 :
    while i!=5:
        talker.publish(roslibpy.Message({'data': False}))
        time.sleep(1)
        i=1+i
if int(sys.argv[3]) == 1 :
    while i!=5:
        talker.publish(roslibpy.Message({'data': True}))
        time.sleep(1)
        i=1+i
