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
rearleftmotor = Motor(Ports.PORT9, GearSetting.RATIO_6_1, True)
rearrightmotor = Motor(Ports.PORT1, GearSetting.RATIO_6_1, False)
frontleftmotor = Motor(Ports.PORT4, GearSetting.RATIO_6_1, True)
frontrightmotor = Motor(Ports.PORT19, GearSetting.RATIO_6_1, False)
armmotor = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
outakemotor = Motor(Ports.PORT6, GearSetting.RATIO_18_1, True)
guidemotor = Motor(Ports.PORT7, GearSetting.RATIO_18_1, False)
stoppermotor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
motorgroupleft = MotorGroup(rearleftmotor, frontleftmotor)
motorgroupright = MotorGroup(rearrightmotor, frontrightmotor)
drivetrain = DriveTrain(motorgroupleft, motorgroupright)
armmotor.set_velocity(100, PERCENT)
outakemotor.set_velocity(100, PERCENT)
driveSpeed = 0
turn = 0
reverse = 0
guide = 0
auton = 0
outakeVariable = 0


def reverse_drive():
    global reverse
    if reverse == 0:
        reverse = 1
        print("reverse")
    else:
        reverse = 0
        print("forward")


def outake_function():
    global outakeVariable
    if outakeVariable == 0:
        outakeVariable = 1
        print("outaking")
        outakemotor.spin(FORWARD)
    else:
        outakeVariable = 0
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


def arm_backward():
    armmotor.spin(REVERSE)


def arm_forward():
    armmotor.spin(FORWARD)


def auton_print():
    if auton == 0:
        controller.screen.clear_screen()
        wait(50, MSEC)
        controller.screen.print("Right Auton")
        wait(50, MSEC)
        controller.screen.set_cursor(3, 1)
    if auton == 1:
        controller.screen.clear_screen()
        wait(50, MSEC)
        controller.screen.print("Short Auton")
        wait(50, MSEC)
        controller.screen.set_cursor(3, 1)
    if auton == 2:
        controller.screen.clear_screen()
        wait(50, MSEC)
        controller.screen.print("Skills Auton")
        wait(50, MSEC)
        controller.screen.set_cursor(3, 1)


def autonomous_switcher():
    global auton
    auton = auton + 1
    if auton > 2:
        auton = 0


def arm_stop():
    armmotor.stop()


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
    if auton == 0:  # Right Auton
        drivetrain.set_drive_velocity(25, PERCENT)
        drivetrain.drive_for(FORWARD, 970, MM)
        arm_forward()
        drivetrain.drive_for(FORWARD, 620, MM, 5, PERCENT)
        arm_stop()
        drivetrain.turn_for(LEFT, 37, DEGREES)
        drivetrain.drive_for(FORWARD, 460, MM, wait=False)
        wait(50, MSEC)
        outakemotor.spin_for(REVERSE, 20000, DEGREES, 25, PERCENT, wait=False)
        armmotor.spin_for(REVERSE, 200000, DEGREES, 20, PERCENT)
    if auton == 1:  # Short Auton
        drivetrain.drive_for(FORWARD, 100, MM)
    if auton == 2:  # Skills Auton
        drivetrain.drive_for(REVERSE, 1000, MM)


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
    controller.buttonX.pressed(outake_function)
    # place driver control in this while loop
    while True:
        motorgroupleft.spin(FORWARD)
        motorgroupright.spin(FORWARD)
        driveSpeed = controller.axis3.position()
        turn = controller.axis1.position()
        if reverse == 0:
            motorgroupleft.set_velocity(driveSpeed + turn, PERCENT)
            motorgroupright.set_velocity(driveSpeed - turn, PERCENT)
        if reverse == 1:
            motorgroupleft.set_velocity(-driveSpeed + turn, PERCENT)
            motorgroupright.set_velocity(-driveSpeed - turn, PERCENT)
        wait(20, MSEC)


# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()
pre_auton()
auton_print()
