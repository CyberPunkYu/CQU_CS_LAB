

from Engine import Engine
from Wheel import Wheel
from Window import Window
from Seat import Seat

class Car:
    def __init__(self):
        self.e = Engine()
        self.wheels = [Wheel(),Wheel(),Wheel(),Wheel()]
        self.frontWindows = [Window(),Window()]
        self.seats = [Seat(),Seat(),Seat(),Seat(),Seat()]
        self.iWeight = 2300

    def pushSpeedPedal(self,offset):
        if offset > 0:
            print("Speed up...")
        else:
            print("Speed down...")

    def pushBrake(self):
        print("Car is slowing down.")

