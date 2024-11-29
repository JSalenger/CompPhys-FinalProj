from WindowSingleton import WindowSingleton
from graphics import update as refresh
from graphics import color_rgb
from time import time
from GNA import GNA

def update(gna):
    """ Will be called as many times as possible. """
    gna()

def fixedUpdate():
    """ Will be called at most _FPS number of times per second. Put costly graphics operations in here. """
    refresh()

    return


if __name__ == '__main__':

    # DrawBG()
    WindowSingleton()
    # bg color 4, 122, 9
    WindowSingleton()().setBackground(color_rgb(0, 0, 0))
    
    # TODO: only add drawing changes to callstack when update is about to be called
    timeSinceUpdate = time()
    _FPS = 30
    _SPF = 1/_FPS # seconds per frame refresh

    gna = GNA([2, 1])

    while True:
        gna.update()

        if time() - timeSinceUpdate > _SPF:
            timeSinceUpdate = time()
            fixedUpdate()