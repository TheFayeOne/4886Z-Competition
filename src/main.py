# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       admin                                                        #
# 	Created:      9/12/2025, 3:18:54 PM                                        #
# 	Description:  Vex V5 Project                                               #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library Imports
from vex import *


brain = Brain()
controller = Controller(PRIMARY)
rearleftmotor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
rearrightmotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
frontleftmotor = Motor(Ports.PORT19, GearSetting.RATIO_18_1, False)
frontrightmotor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
armmotor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
motorgroupleft = MotorGroup(rearleftmotor, frontleftmotor)
motorgroupright = MotorGroup(rearrightmotor, frontrightmotor)
drivetrain = DriveTrain(motorgroupleft, motorgroupright)
drivespeed = 0
armspeed = 0
turn = 0
reverse = 0

def reverse_drive():
    global reverse
    if reverse == 0:
        reverse = 1
        print("reverse")
    else:
        reverse = 0
        print("forward")

def arm_backward():
    armmotor.spin(FORWARD, 100, PERCENT)

def arm_forward():
    armmotor.spin(REVERSE, 100, PERCENT)

def arm_stop():
    armmotor.stop()

def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("Autonomous Code")
    # place automonous code here
    drivetrain.set_drive_velocity(50, PERCENT)
    drivetrain.drive_for(FORWARD, 500, MM)

def user_control():
    brain.screen.clear_screen()
    brain.screen.print("User Control")
    drivetrain.set_drive_velocity(0, PERCENT)
    controller.buttonL1.pressed(arm_backward)
    controller.buttonL1.released(arm_stop)
    controller.buttonR1.pressed(arm_forward)
    controller.buttonR1.released(arm_stop)
    controller.buttonY.pressed(reverse_drive)
    # place driver control in this while loop
    while True:
        motorgroupleft.spin(FORWARD)
        motorgroupright.spin(FORWARD)
        drivespeed = controller.axis3.position()
        turn = controller.axis1.position()
        if reverse == 0:
            motorgroupleft.set_velocity(-drivespeed + turn, PERCENT)
            motorgroupright.set_velocity(-drivespeed - turn, PERCENT)
        if reverse == 1:
            motorgroupleft.set_velocity(drivespeed - turn, PERCENT)
            motorgroupright.set_velocity(drivespeed + turn, PERCENT)

        wait(20, MSEC)

# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()