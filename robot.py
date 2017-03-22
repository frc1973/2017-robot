#!/usr/bin/env python3

import wpilib
from magicbot import MagicRobot

class MyRobot(MagicRobot):

    #
    # Define components here
    #

    def createObjects(self):
        """Initialize all wpilib motors & sensors"""

        # camera
        # utrasoni sensors
        # motors
        self.myRobot = wpilib.RobotDrive(0,1)
        self.myRobot.setSafetyEnabled(False)

        #2Joysticks
        self.leftStick = wpilib.Joystick(0)
        self.rightStick = wpilib.Joystick(1)

        # 5 motor controlors: 1colocter, 2 for weels, 1 for shooter
        #light
        #lifter: 1 motor
        #

        self.gyro = wpilib.ADXRS450_Gyro()



    def teleopPeriodic(self):
        """Place code here that does things as a result of operator
           actions. This code gets called over and over again, do not
           put a loop in"""

        self.myRobot.arcadeDrive(self.leftStick, True)

if __name__ == '__main__':
    wpilib.run(MyRobot)
