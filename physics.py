#
# See the documentation for more details on how this works
#
# The idea here is you provide a simulation object that overrides specific
# pieces of WPILib, and modifies motors/sensors accordingly depending on the
# state of the simulation. An example of this would be measuring a motor
# moving for a set period of time, and then changing a limit switch to turn
# on after that period of time. This can help you do more complex simulations
# of your robot code without too much extra effort.
#
# NOTE: THIS API IS ALPHA AND WILL MOST LIKELY CHANGE!
#       ... if you have better ideas on how to implement, submit a patch!
#

from pyfrc.physics import drivetrains

try:
    from pyfrc.physics.visionsim import VisionSim
except ImportError:
    VisionSim = None
    
from networktables import NetworkTables

#from components.drive import Drive


class PhysicsEngine(object):
    '''
        Simulates a motor moving something that strikes two limit switches,
        one on each end of the track. Obviously, this is not particularly
        realistic, but it's good enough to illustrate the point
    '''

    def __init__(self, physics_controller):
        '''
            :param physics_controller: `pyfrc.physics.core.PhysicsInterface` object
                                       to communicate simulation effects to
        '''

        self.physics_controller = physics_controller
        self.position = 0

        self.ft_per_sec = 5
        self.wheel_circumference = 18.8

        self.physics_controller.add_device_gyro_channel('adxrs450_spi_4_angle')
        
        if VisionSim is not None:
            targets = [
                # right
                VisionSim.Target(16, 12, 250, 20), # angle is 122.23
                # middle
                VisionSim.Target(18.5, 16, 295, 65), # angle is 180
                # left
                VisionSim.Target(16, 20, 340, 110), # angle is -142
            ]
            
            self.vision = VisionSim(targets, 61.0,
                                    1.5, 15, 15)
        else:
            self.vision = None
            
    @property
    def nt(self):
        try:
            return self._nt
        except AttributeError:
            self._nt = NetworkTables.getTable('/')
            return self._nt

    def update_sim(self, hal_data, now, tm_diff):
        '''
            Called when the simulation parameters for the program need to be
            updated.

            :param now: The current time as a float
            :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
        '''

        # Simulate the drivetrain
        l_motor = hal_data['pwm'][0]['value']
        r_motor = hal_data['pwm'][1]['value']

        speed, rotation = drivetrains.two_motor_drivetrain(l_motor, r_motor, speed=self.ft_per_sec)
        self.physics_controller.drive(speed, rotation, tm_diff)

        # Inches we traveled
        distance_inches = 12.0*speed*tm_diff

        # Use that to give a rough approximation of encoder values.. not
        # accurate for turns, but we don't need that
        # -> encoder = distance / (wheel_circumference / 360.0)

        hal_data['encoder'][0]['count'] += int(distance_inches / (self.wheel_circumference/360.0))
        
        if self.vision:
            x, y, angle = self.physics_controller.get_position()
            
            data = self.vision.compute(now, x, y, angle)
            if data is not None:
                self.nt.putNumberArray('/camera/target', data[0][:3])
        
