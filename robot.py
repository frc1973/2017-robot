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

        self.left_motor = wpilib.Spark(0)
        self.right_motor = wpilib.Spark(1)

        self.lifter_motor = wpilib.Talon(2)


        self.myRobot = wpilib.RobotDrive(self.left_motor, self.right_motor)
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

        if self.rightStick.getTrigger():
            self.lifter_motor.set(self.rightStick.getY())
        else:
            self.lifter_motor.set(0)

if __name__ == '__main__':
    wpilib.run(MyRobot)
