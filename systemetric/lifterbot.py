from robot import Robot
from blindmotordriver import BlindMotorDriver
from sr2013 import VisionShim
from devices import Mbed, MotorMbed, Arm, Pump

class LifterBot(Robot):
    def __init__(self, visionMode):
        self.mbed = Mbed('/dev/ttyACM0', 115200)
        self.vision = VisionShim('/dev/video0')
        self.visionMode = visionMode
        self.leftMotor = MotorMbed(self.mbed, 0)
        self.rightMotor = MotorMbed(self.mbed, 1)
        self.motorDriver = BlindMotorDriver(self.leftMotor, self.rightMotor,
                                            1, -1, 1, 0.5) #left, right, dist, turn
        self.arm = Arm(self.mbed)
        self.pump = Pump(self.mbed)

        super(LifterBot, self).__init__()
