#!/usr/bin/env python3

import wpilib
from magicbot import MagicRobot

class MyRobot(MagicRobot):
    
    #
    # Define components here
    #
    
    def createObjects(self):
        """Initialize all wpilib motors & sensors"""
        
    def teleopPeriodic(self):
        """Place code here that does things as a result of operator
           actions. This code gets called over and over again, do not
           put a loop in"""
           
if __name__ == '__main__':
    wpilib.run(MyRobot)