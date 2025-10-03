# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       admin                                                        #
# 	Created:      9/12/2025, 3:18:54 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *


brain = Brain()
controller = Controller(PRIMARY)
rearleftmotor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
rearrightmotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
frontleftmotor = Motor(Ports.PORT19, GearSetting.RATIO_18_1, False)
frontrightmotor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
motorgroupleft = MotorGroup(rearleftmotor, frontleftmotor)
motorgroupright = MotorGroup(rearrightmotor, frontrightmotor)
drivetrain = DriveTrain(motorgroupleft, motorgroupright)


def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("Autonomous Code")
    drivetrain.set_drive_velocity(50, PERCENT)
    drivetrain.drive_for(FORWARD, 500, MM)
    # place automonous code here

def user_control():
    brain.screen.clear_screen()
    brain.screen.print("User Control")
    drivetrain.set_drive_velocity(0, PERCENT)
    # place driver control in this while loop
    while True:
        motorgroupleft.spin(FORWARD)
        motorgroupright.spin(FORWARD)
        speed = controller.axis3.position()
        turn = controller.axis1.position()         
        motorgroupleft.set_velocity(speed + turn, PERCENT)
        motorgroupright.set_velocity(speed - turn, PERCENT)
        wait(20, MSEC)

# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()
speed = 0
turn = 0