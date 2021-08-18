#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

def callback(data):
    global lock
    global counter_lock
    
    twist = Twist()

    print(data)

    # Controller unlocking/locking, Ps4 Button
    if data.buttons[10] == 1:
        counter_lock += 1
        print("counter_lock: ", str(counter_lock))
        if counter_lock >= 10:
            lock = not lock
    else:
        counter_lock = 0

    # Driving, L2(forward) and R2(backward)
    if not lock:
        if data.axes[5] == 1:
            twist.linear.x = abs((data.axes[2]+1 - 2)/2)*4
        else:
            twist.linear.x = abs((data.axes[5]+1 - 2)/2)*-4

        twist.angular.z = data.axes[3]

    pub.publish(twist)
 



def start():
    global pub
    global lock
    global counter_lock

    # locks the controller
    lock = True
    counter_lock = 0

    rospy.init_node("steering", anonymous=False)

    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

    rospy.Subscriber("joy", Joy, callback)

    rospy.spin()

if __name__=='__main__':
    try:
        start()
    except rospy.ROSInitException:
        pass

