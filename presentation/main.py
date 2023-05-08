from V import V
from WindowSingleton import WindowSingleton
from graphics import update as refresh
from graphics import Circle, Point, color_rgb, Rectangle
from time import time
from Orrery import Orrery
from Celestial import Celestial
from GNA import GNA

def decreaseDeviationCallback(self):
    self.stdDev /= 1.1

def decreaseDtCallback(self):
    if self.epoch == 2:
        for i in self.populates:
            i.startingDt = .02
            i.dt = .02
        print("Updated dt of populates to be: " + str(self.populates[0].dt))
    if self.epoch == 4:
        for i in self.populates:
            i.startingDt = .01
            i.dt = .01
        print("Updated dt of populates to be: " + str(self.populates[0].dt))

def decreasePopulationCallback(self):
    if self.epoch == 3:
        self.familySizes = [50, 45, 30, 30, 25, 20, 20, 15, 15, 10, 10, 10, 5, 5, 5, 5]
        print("Updated family sizes for next generation to be: [50, 45, 30, 30, 25, 20, 20, 15, 15, 10, 10, 10, 5, 5, 5, 5] (sum: " 
            + str(sum(self.familySizes)) + ")")

def update(gna):
    """ Will be called as many times as possible. """
    gna()

def fixedUpdate(gna):
    """ Will be called at most _FPS number of times per second. Put costly graphics operations in here. """
    refresh()
    gna()

    return


if __name__ == '__main__':
    generation = 0

    # DrawBG()
    WindowSingleton()
    # bg color 4, 122, 9
    WindowSingleton()().setBackground(color_rgb(0, 0, 0))
    
    # TODO: only add drawing changes to callstack when update is about to be called
    timeSinceUpdate = time()
    _FPS = 30
    _SPF = 1/_FPS # seconds per frame refresh

    gna = GNA(.03, [1], Orrery, .03, [], True)


    while True:
        # update(gna)


        if time() - timeSinceUpdate > _SPF:
            timeSinceUpdate = time()
            fixedUpdate(gna)