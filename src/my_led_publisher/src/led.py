#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import os
import time

def publish_led_data(pub, file_path):
    last_modified = os.stat(file_path).st_mtime  # Initial file modification time
    try:
        while not rospy.is_shutdown():
            current_modified = os.stat(file_path).st_mtime
            if current_modified != last_modified:
                with open(file_path, 'r') as file:
                    data = file.read().strip()  # Read the string from the file
                    pub.publish(data)  # Publish the string to the specified topic
                    rospy.loginfo("Published: %s", data)
                    last_modified = current_modified  # Update the last modified time

            time.sleep(0.1)  # Small delay to avoid excessive checking

    except rospy.ROSInterruptException:
        pass

def led_publisher():
    rospy.init_node('led_publisher', anonymous=True)

    leddata1_pub = rospy.Publisher('leddata1', String, queue_size=10)
    leddata2_pub = rospy.Publisher('leddata2', String, queue_size=10)

    file_path_leddata1 = 'data1.txt'  # Update with your file path for leddata1
    file_path_leddata2 = 'data2.txt'  # Update with your file path for leddata2

    try:
        # Publish to leddata1
        publish_led_data(leddata1_pub, file_path_leddata1)

        # Publish to leddata2
        publish_led_data(leddata2_pub, file_path_leddata2)

    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    led_publisher()

