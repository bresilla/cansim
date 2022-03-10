import cv2
import base64
import logging
import time
import sys
import roslibpy

from cv_bridge import CvBridge
bridge = CvBridge()
encoding_format="rgb8"

client = roslibpy.Ros(host=sys.argv[1], port=int(sys.argv[2]))
while not client.is_connected:
    try:
        client.run()
    except:
        time.sleep(5)
        print("NOT CONNECTED")

camera_topic = roslibpy.Topic(client, '/aaaa', 'sensor_msgs/Image')

def send2topic(topic, message):
    topic.publish(roslibpy.Message(message))
    print(message)


vid = cv2.VideoCapture(0)
while(True):
    ret, frame = vid.read()
    cv2.imshow('frame', frame)
    encoded = bridge.cv2_to_imgmsg(frame, "bgr8")
    print(type(encoded))
    print(encoded.data)
    
    send2topic(camera_topic, {
        "header": encoded.data,
        "height": encoded.height,
        "width": encoded.width,
        "step": encoded.step,
        "is_bigendian": encoded.is_bigendian,
        "data": encoded.data
    })

    # print(encoded["header"])
    print("\n\n\n\n\n")



    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
