from V import V
from typing import Union
from graphics import Circle, Point, color_rgb
from WindowSingleton import WindowSingleton

class Planet:
    def __init__(self, initialPosition: V, initialVelocity: V, mass: Union[float, int], color):
        self.position = initialPosition
        self.initialPosition = initialPosition

        self.velocity = initialVelocity
        self.initialVelocity = initialVelocity

        self.acceleration = V(0, 0, 0)

        self.mass = mass
        self.color = color

        self.delta_pos = V(0, 0, 0)

        self.tempPosition = V(0, 0, 0)
        self.tempVelocity = V(0, 0, 0)
        self.tempAcceleration = V(0, 0, 0)

        self.radius = .2

        self.sphere = Circle(Point(self.position.x, self.position.y), .1)
        self.sphere.setFill(self.color)
        self.sphere.draw(WindowSingleton()())


    def setTempVals(self, pos: V, vel: V, acc: V):
        self.tempPosition = pos
        self.tempVelocity = vel
        self.tempAcceleration = acc

    def pushTempVals(self):
        self.position = self.tempPosition
        self.velocity = self.tempVelocity
        self.acceleration = self.tempAcceleration

    def setColor(self, color):
        self.sphere.undraw()
        self.sphere.setFill(color)
        self.sphere.draw(WindowSingleton()())

    def handleUndraw(self):
        self.sphere.undraw()

    def draw(self):
        self.sphere.move(self.delta_pos.x, self.delta_pos.y)
