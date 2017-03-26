#!/usr/bin/env python3

import wpilib
from magicbot import MagicRobot

from components.drivetrain import DriveTrain

class MyRobot(MagicRobot):

    #
    # Define components here
    #

    drivetrain = DriveTrain

    def createObjects(self):
        """Initialize all wpilib motors & sensors"""

        # camera
        # utrasoni sensors
        # motors

        self.robot = self

        self.left_motor = wpilib.Spark(0)
        self.right_motor = wpilib.Spark(1)
        self.left_motor.setInverted(True)
        self.right_motor.setInverted(True)

        self.lifter_motor = wpilib.Talon(2)

        self.ultrasonic = wpilib.AnalogInput(0)

        self.light_relay = wpilib.Relay(0)
        self.light_relay.set(wpilib.Relay.Value.kOn)

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

        wpilib.CameraServer.launch()

    def teleopPeriodic(self):
        """Place code here that does things as a result of operator
           actions. This code gets called over and over again, do not
           put a loop in"""

        self.drivetrain.move(self.leftStick.getY(), self.leftStick.getX())

        if self.leftStick.getTrigger():
            self.drivetrain.driveToWall()

        if not self.rightStick.getTrigger():
            if self.leftStick.getRawButton(10):
                self.drivetrain.move(-self.leftStick.getY(), self.leftStick.getX())
                self.lifter_motor.set(1)
            else:
                self.lifter_motor.set(0)
        if self.rightStick.getTrigger():
            self.lifter_motor.set(self.rightStick.getY())

if __name__ == '__main__':
    wpilib.run(MyRobot)
