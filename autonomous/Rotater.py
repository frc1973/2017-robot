from magicbot import AutonomousStateMachine, timed_state, state
import wpilib
class Rotater (AutonomousStateMachine):

    def _init_  (self, robot, FOUND, DISTANCE):

        if self.LASTTM<TM:
           self.FOUND=FOUND
           self.LASTTM=TM
           self.TARGET=RA-OFFSET

        if self.FOUND:
            OFFSET=RA-self.TARGET
            x=Px*OFFSET
            if abs(OFFSET)<10:
               Y=Py*(DISTANCE)
