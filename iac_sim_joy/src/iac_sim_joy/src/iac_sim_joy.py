#! /usr/bin/python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Header, Float32, UInt8
from autonoma_msgs.msg import VehicleInputs

import pygame
from pygame import JOYAXISMOTION, JOYBUTTONDOWN, JOYBUTTONUP, JOYDEVICEADDED, JOYDEVICEREMOVED, JOYHATMOTION
import time

pygame.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print('Current Joystick:' + pygame.joystick.Joystick(0).get_name())
motion = [0, 0 ,0, 0, 0 ,0] 
pygame.joystick.init()
j_thr = 0.0
j_brk = 0.0
j_ste = 0.0
g_input = 1



class IAC_joy_pub(Node):
    def __init__(self):
        super().__init__('vehicle_inputs')
        self.pub = self.create_publisher(VehicleInputs, 'vehicle_inputs', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)


    def timer_callback(self):
        global j_thr
        global j_brk
        global j_ste
        global g_input

        for event in pygame.event.get():
            if event.type == JOYDEVICEADDED:
                joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
            if event.type == JOYDEVICEREMOVED:
                joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
            if event.type == JOYAXISMOTION:
                # Throttle (0 - 100)
                if event.axis == 5:
                    motion[event.axis] = event.value
                    j_thr = (event.value*50+50)
                    #print(j_thr)
                
                # Brake (0 - 6000)
                if event.axis == 2:
                    motion[event.axis] = event.value
                    j_brk = ((event.value*50+50)*60)
                    print(j_brk)
                
                # Steering (-240 - 240) 
                if event.axis == 0:
                    motion[event.axis] = event.value
                    j_ste = (-(event.value*240))
                    #print(j_ste)
            # Gear
            if event.type == JOYBUTTONDOWN:
                if event.button == 5:
                    g_input = g_input + 1
                elif event.button == 4:
                    g_input = g_input - 1

                # Gear range 1~6
                if g_input < 1:
                    g_input = 1
                if g_input > 6:
                    g_input = 6

        msg = VehicleInputs()
        msg.header = Header()
        msg.throttle_cmd = j_thr
        msg.throttle_cmd_count = 1
        msg.brake_cmd = j_brk
        msg.brake_cmd_count = 1
        msg.steering_cmd = j_ste
        msg.steering_cmd_count = 1
        msg.gear_cmd = g_input

        self.pub.publish(msg)
        self.get_logger().info('Publishing: %s' % msg)

def main(args=None):
    rclpy.init(args = args)
    publisher = IAC_joy_pub()
    rclpy.spin(publisher)
    publisher.destroy_node()
    pygame.joystick.quit()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
