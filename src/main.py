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
rearleftmotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
rearrightmotor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
frontleftmotor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
frontrightmotor = Motor(Ports.PORT19, GearSetting.RATIO_18_1, True)
armmotortop = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
armmotorbottom = Motor(Ports.PORT9, GearSetting.RATIO_18_1, True)
blockermotor = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
guidemotor = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
motorgroupleft = MotorGroup(rearleftmotor, frontleftmotor)
motorgroupright = MotorGroup(rearrightmotor, frontrightmotor)
motorgrouparm = MotorGroup(armmotortop, armmotorbottom)
drivetrain = DriveTrain(motorgroupleft, motorgroupright)
motorgrouparm.set_velocity(100, PERCENT)
blockermotor.set_velocity(100, PERCENT)
drivespeed = 0
turn = 0
reverse = 0
guide = 0
blocking = 1

def reverse_drive():
    global reverse
    if reverse == 0:
        reverse = 1
        print("reverse")
    else:
        reverse = 0
        print("forward")

def arm_blocking():
    global blocking
    if blocking == 0:
        blocking = 1
        blockermotor.spin(FORWARD)
        wait(0.85, SECONDS)
        blockermotor.stop()
        print("blocking activated")

    else:
        blocking = 0
        blockermotor.spin(REVERSE)
        wait(0.85, SECONDS)
        blockermotor.stop()
        print("blocking deactivated")

def guide_toggle():
    global guide
    if guide == 0:
        guide = 1
        guidemotor.spin(REVERSE)
        wait(0.8, SECONDS)
        guidemotor.stop()
        print("guide activated")

    else:
        guide = 0
        guidemotor.spin(FORWARD)
        wait(0.9, SECONDS)
        guidemotor.stop()
        print("guide deactivated")

def arm_backward():
    motorgrouparm.spin(REVERSE)

def arm_forward():
    motorgrouparm.spin(FORWARD)

def arm_stop():
    motorgrouparm.stop()

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
    controller.buttonB.pressed(arm_blocking)
    controller.buttonB.pressed(guide_toggle)
    # place driver control in this while loop
    while True:
        motorgroupleft.spin(FORWARD)
        motorgroupright.spin(FORWARD)
        drivespeed = controller.axis3.position()
        turn = controller.axis1.position()
        if reverse == 0:
            motorgroupleft.set_velocity(drivespeed + turn, PERCENT)
            motorgroupright.set_velocity(drivespeed - turn, PERCENT)
        if reverse == 1:
            motorgroupleft.set_velocity(-drivespeed + turn, PERCENT)
            motorgroupright.set_velocity(-drivespeed - turn, PERCENT)

        wait(20, MSEC)

# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()