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
armmotortop = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
armmotorbottom = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
motorgrouparm = MotorGroup(armmotortop, armmotorbottom)
outakemotor = Motor(Ports.PORT6, GearSetting.RATIO_18_1, True)
guidemotor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
stoppermotor = Motor(Ports.PORT7, GearSetting.RATIO_18_1, True)
motorgroupleft = MotorGroup(rearleftmotor, frontleftmotor)
motorgroupright = MotorGroup(rearrightmotor, frontrightmotor)
drivetrain = DriveTrain(motorgroupleft, motorgroupright)
armmotortop.set_velocity(100, PERCENT)
armmotorbottom.set_velocity(100, PERCENT)
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

def stopper_open():
    print("stopper opened")
    stoppermotor.spin(FORWARD)
    wait(0.4, SECONDS)
    stoppermotor.stop()

def stopper_close():
   print("stopper closed")
   stoppermotor.spin(REVERSE)
   wait(0.4, SECONDS)
   stoppermotor.stop() 

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
    motorgrouparm.spin(REVERSE)

def arm_forward():
    motorgrouparm.spin(FORWARD)

def auton_print():
    if auton == 0 or 2:
        controller.screen.clear_screen()
        wait(50, MSEC)
        controller.screen.print("Auton 1")
        wait(50, MSEC)
        controller.screen.set_cursor(3, 1)
    if auton == 1:
        controller.screen.clear_screen()
        wait(50, MSEC)
        controller.screen.print("Auton 2")
        wait(50, MSEC)
        controller.screen.set_cursor(3, 1)

def autonomous_switcher():
    global auton
    auton = auton + 1
    if auton > 1:
        auton = 0

def button_pass():
    pass

def arm_stop():
    motorgrouparm.stop()
 
def pre_auton():
    global auton
    brain.screen.clear_screen()
    brain.screen.print("Pre-Autonomous")
    controller.buttonA.pressed(autonomous_switcher)
    controller.buttonA.pressed(auton_print)

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
    controller.buttonR2.pressed(stopper_open)
    controller.buttonL2.pressed(stopper_close)
    controller.buttonY.pressed(reverse_drive)
    controller.buttonX.pressed(outake)
    controller.buttonUp.pressed(guide_toggle)
    outake()
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