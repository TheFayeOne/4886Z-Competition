# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Kelvin Morse                                                 #
# 	Created:      9/12/2025, 3:18:54 PM                                        #
# 	Description:  Vex V5 Project                                               #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library Imports
from vex import *


brain = Brain()
controller = Controller(PRIMARY)
rearleftmotor = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)
rearrightmotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
frontleftmotor = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
frontrightmotor = Motor(Ports.PORT19, GearSetting.RATIO_18_1, True)
armmotor = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
outakemotor = Motor(Ports.PORT6, GearSetting.RATIO_18_1, True)
guidemotor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
motorgroupleft = MotorGroup(rearleftmotor, frontleftmotor)
motorgroupright = MotorGroup(rearrightmotor, frontrightmotor)
drivetrain = DriveTrain(motorgroupleft, motorgroupright)
armmotor.set_velocity(100, PERCENT)
outakemotor.set_velocity(100, PERCENT)
drivespeed = 0
turn = 0
reverse = 0
guide = 0
auton = 0
outake = 0

def reverse_drive():
    global reverse
    if reverse == 0:
        reverse = 1
        print("reverse")
    else:
        reverse = 0
        print("forward")

def outake():
    global outake
    if outake == 0:
        outake = 1
        print("outaking")
        outakemotor.spin(FORWARD)
    else:
        outake = 0
        print("not outaking")
        outakemotor.stop()

def guide_toggle():
    global guide
    if guide == 0:
        guide = 1
        guidemotor.spin(REVERSE)
        wait(0.55, SECONDS)
        guidemotor.stop()
        print("guide activated")

    else:
        guide = 0
        guidemotor.spin(FORWARD)
        wait(0.65, SECONDS)
        guidemotor.stop()
        print("guide deactivated")

def arm_backward():
    armmotor.spin(REVERSE)

def arm_forward():
    armmotor.spin(FORWARD)

def auton_print():
    if auton == 0 or 2:
        brain.screen.print_at("1", x=100, y=50)
    if auton == 1:
        brain.screen.print_at("2", x=100, y=50)

def autonomous_switcher():
    global auton
    auton = auton + 1
    if auton > 1:
        auton = 0

def arm_stop():
    armmotor.stop()

    global auton
    auton = auton + 1
    if auton > 1:
        auton = 0
 
def pre_auton():
    global auton
    brain.screen.clear_screen()
    brain.screen.print("Pre-Autonomous")
    brain.screen.pressed(autonomous_switcher)
    brain.screen.pressed(auton_print)

def autonomous():
    global auton
    brain.screen.clear_screen()
    brain.screen.print("Autonomous Code")
    # place automonous code here
    drivetrain.set_drive_velocity(50, PERCENT)
    global auton
    if auton == 0:
        drivetrain.drive_for(FORWARD, 500, MM)
    if auton == 1:
        drivetrain.drive_for(FORWARD, 100, MM)

def user_control():
    brain.screen.clear_screen()
    brain.screen.print("User Control")
    drivetrain.set_drive_velocity(0, PERCENT)
    controller.buttonL1.pressed(arm_backward)
    controller.buttonL1.released(arm_stop)
    controller.buttonR1.pressed(arm_forward)
    controller.buttonR1.released(arm_stop)
    controller.buttonY.pressed(reverse_drive)
    controller.buttonA.pressed(outake)
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
pre_auton()
auton_print()