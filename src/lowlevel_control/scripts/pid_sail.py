#!/usr/bin/env python

import rospy
import numpy as np
from std_msgs.msg import Float32, UInt16, String

from lowlevel_control.sail_data import Sail_data

sail = Sail_data()
saildata = rospy.get_param('/sail')
pullypivotdistance = saildata['pullypivotDistance']
boomsheetdistance = saildata['boomsheetDistance']

def node_publisher():
    pub = rospy.Publisher('/sail_servo', UInt16, queue_size=10)
    rospy.init_node('sail_servo', anonymous=True)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        sail_angle = 0.5*sail.apparent_wind_angle()
        sheetlength = np.sqrt(pullypivotdistance**2+boomsheetdistance**2-2*pullypivotdistance*boomsheetdistance*np.cos(sail_angle/180*np.pi))
        angle = sheetlength/1000/saildata['winchDiameter']/np.pi*180
        pub.publish(int(angle))

        rate.sleep()


if __name__ == '__main__':
    try:
        rospy.Subscriber('/apparent_wind_direction', Float32, sail.update_apparent_wind_angle)
        node_publisher()
    except rospy.ROSInterruptException:
        pass