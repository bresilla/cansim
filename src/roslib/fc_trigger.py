import roslibpy
import sys
import time

client=roslibpy.Ros(host= sys.argv[1], port= int(sys.argv[2]))
client.run()
print(client.is_connected)
talker=roslibpy.Topic(client,'/lsp1/computer_on','std_msgs/Bool')
i=0

while True:
    talker.publish(roslibpy.Message({'data': True}))
    time.sleep(1)
    i=1+i
