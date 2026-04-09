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
inertial = Inertial(Ports.PORT21)
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
drivetrain = SmartDrive(motorgroupleft, motorgroupright, inertial, 260, 305, 255, MM)
descorerpiston = Pneumatics(brain.three_wire_port.a)
armmotor.set_velocity(100, PERCENT)
outakemotor.set_velocity(100, PERCENT)
driveSpeed = 0
turn = 0
reverse = 0
guide = 0
auton = 0
outakeVariable = 0
descorerVariable = 0

<<<<<<< HEAD

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

=======
def autonomous_switcher():
    global auton
    auton = auton + 1
    if auton > 3:
        auton = 0
>>>>>>> c12d762ddc9e0be1a8cf98c415ecea06f8b71f7f

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
        controller.screen.print("Left Auton")
        wait(50, MSEC)
        controller.screen.set_cursor(3, 1)
    if auton == 2:
        controller.screen.clear_screen()
        wait(50, MSEC)
        controller.screen.print("Short Auton")
        wait(50, MSEC)
        controller.screen.set_cursor(3, 1)
    if auton == 3:
        controller.screen.clear_screen()
        wait(50, MSEC)
        controller.screen.print("Skills Auton")
        wait(50, MSEC)
        controller.screen.set_cursor(3, 1)
    controller.rumble("-")

def pre_auton():
    global auton
    brain.screen.clear_screen()
    brain.screen.print("Pre-Autonomous")
    controller.buttonA.pressed(autonomous_switcher)
    controller.buttonA.pressed(auton_print)
    inertial.calibrate()

def arm_forward():
    armmotor.spin(FORWARD)

def arm_backward():
    armmotor.spin(REVERSE)

def arm_stop():
    armmotor.stop()

def autonomous():
    global auton
    brain.screen.clear_screen()
    brain.screen.print("Autonomous Code")
    # place automonous code here
    drivetrain.set_drive_velocity(50, PERCENT)
    if auton == 0:  # Right Auton
        drivetrain.set_drive_velocity(25, PERCENT)
        drivetrain.drive_for(FORWARD, 850, MM)
        arm_forward()
        drivetrain.drive_for(FORWARD, 645, MM, 5, PERCENT)
        arm_stop()
        drivetrain.turn_to_heading(-52, DEGREES)
        drivetrain.drive_for(FORWARD, 350, MM, wait=True)
        drivetrain.drive_for(REVERSE, 100, MM, wait=True)
        wait(50, MSEC)
        outakemotor.spin_for(REVERSE, 2500, DEGREES, 25, PERCENT, wait=False)
        armmotor.spin_for(REVERSE, 2500, DEGREES, 23, PERCENT, wait=False)
    if auton == 1: #Left Auton
        drivetrain.set_drive_velocity(25, PERCENT)
        drivetrain.drive_for(REVERSE, 1200, MM)
        drivetrain.turn_to_heading(54, DEGREES)
        drivetrain.drive_for(REVERSE, 260, MM)
        arm_forward()
        outakemotor.spin_for(FORWARD, 5000, DEGREES, 100, PERCENT)
    if auton == 2:  # Short Auton
        drivetrain.drive_for(FORWARD, 100, MM)
    if auton == 3:  # Skills Auton
        drivetrain.drive_for(REVERSE, 1000, MM)

def stopper_open():
    controller.rumble(".")
    print("stopper opened")
    stoppermotor.spin(FORWARD)
    wait(0.3, SECONDS)
    stoppermotor.stop()
    controller.rumble(".")

def stopper_close():
    controller.rumble(".")
    print("stopper closed")
    stoppermotor.spin(REVERSE)
    wait(0.4, SECONDS)
    stoppermotor.stop()
    controller.rumble(".")

def outake_function():
    global outakeVariable
    if outakeVariable == 0:
        outakeVariable = 1
        print("outaking")
        outakemotor.spin(FORWARD)
        controller.rumble(".")
    else:
        outakeVariable = 0
        print("not outaking")
        outakemotor.stop()
        controller.rumble(".")

def descorer_function():
    global descorerVariable
    if descorerVariable == 0:
        descorerpiston.open()
        descorerVariable = 1
        print("descorer opened")
    else:
        descorerpiston.close()
        descorerVariable = 0
        print("descorer closed")

def reverse_drive():
    global reverse
    if reverse == 0:
        reverse = 1
        print("reverse")
        controller.rumble("-")
    else:
        reverse = 0
        print("forward")
        controller.rumble("-")

def user_control():
    brain.screen.clear_screen()
    brain.screen.print("User Control")
    drivetrain.set_drive_velocity(0, PERCENT)
    global auton
    controller.buttonL1.pressed(arm_backward)
    controller.buttonL1.released(arm_stop)
    controller.buttonR1.pressed(arm_forward)
    controller.buttonR1.released(arm_stop)
    controller.buttonR2.pressed(stopper_open)
    controller.buttonL2.pressed(stopper_close)
    controller.buttonUp.pressed(reverse_drive)
    controller.buttonB.pressed(outake_function)
    controller.buttonX.pressed(descorer_function)
    if auton == 0:
        outakemotor.stop()
    if auton == 1:
        stopper_close()
        arm_stop()
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
controller.rumble("-")