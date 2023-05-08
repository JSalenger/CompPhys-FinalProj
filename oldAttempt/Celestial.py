from typing import List
from V import V
from graphics import Circle, Point, color_rgb
from WindowSingleton import WindowSingleton

class Celestial:
    """
    Constructs a celestial (an object which hangs out in space; kinda chillin)
    It should be used for objects which gravitational pull is strong enough to effect others
    They can be added as dependencies to other Celestials and also be added to
    Orrery objects

    :param position: The initial position of the object in space
    """
    def __init__(self, position: V, velocity: V, mass: float, color = color_rgb(242, 232, 41)) -> None:
        # The initial position of the object
        self.position = position
        self.iPosition = V(position.x, position.y, position.z)
        # The initial velocity 
        self.velocity = velocity
        self.iVelocity = V(velocity.x, velocity.y, velocity.z)
        # Stores the list of all dependencies of this object (all objects which are close enough to effect its orbit)
        self.dependencies: List[Celestial] = []
        # mass mmmmmmmmmmmm
        self.mass = mass

        self.id = -1
        
        self.step = 0

        self.radius = .05

        self.positionQueue = position
        self.totalDistanceTraveled = V(0, 0, 0)

        self.sphere = Circle(Point(self.position.x, self.position.y), .05)
        self.sphere.setFill(color)
        self.sphere.draw(WindowSingleton()())

        self.color = color

        self.died = False
        self.diedFromBeingTooFar = False

        self.Gmags = []

    """
    Adds a "dependency" (a celestial close enough to the body to affect its orbit) to this objects
    dependency list in order to include it in its calculations

    :returns: None
    """
    def addDependency(self, celestial) -> None:
        self.dependencies.append(celestial)

    """
    Get the current position of the celestial (does not calculate a new position)

    :returns: A vector of the current position
    """
    def getPosition(self) -> V:
        return self.position
    
    """
    Interface to make setting dependencies easier.
    
    :returns: None
    """
    def automateDependencies(self, celestials):
        if self.id == -1:
            print("You must assign an ID to every planet before calling automateDependencies")
            raise Exception("You must assign an ID to every planet before calling automateDependencies")
        
        for v in celestials:
            # print(v.id)
            if v.id == self.id:
                continue
                
            self.dependencies.append(v)

        # print(len(self.dependencies))
                

        # print("Dependencies set for planet (" + str(self.id) + "). ; " + str(self.dependencies) + "(" + str(len(self.dependencies)) + ")")
            
    
    """
    Get the next position of the celestial and update it inplace if keepHistory is true append old position to
    histories array

    :returns: A vector of the next position
    """
    def putNextPositionInQueue(self, dt: float = .000001, isFirst = False) -> V:
        self.step += 1 # inc. step to mark which position we are on
        # Calculate force of gravity for each item in the 
        for celestial in self.dependencies:
            # Calculate the distance between masses
            # vector in direction of Other -----> Self
            distance = celestial.position-self.position
            # Calculate magnitude of force of gravity 
            Gmag = 6.674e-11 * ((celestial.mass * self.mass)/(distance.m * distance.m))

            self.Gmags.append(Gmag * 1e-5)

            
            if Gmag > 1e-2:
                dt = .01
            elif Gmag > 1e-5:
                dt = .001
            elif Gmag > 1e-9:
                dt = .001
            else: 
                dt = .001


            # completely arbitrary :P
            if Gmag < 7e-13:
                self.died = True
                self.diedFromBeingTooFar = True
                # print("Die from too far")

            # Apply the force of gravity to both celestials (if do both is true)
            F_g = distance(Gmag)

            # F = ma || F/m = a
            acceleration = (F_g / self.mass)
            # Calculate approx. for given dt
            self.velocity += acceleration * dt
            self.positionQueue = self.position + self.velocity * dt
            self.totalDistanceTraveled += abs(self.velocity * dt)

            if isFirst:
                return dt
        

    """
    Push next in Queue into the current position slot. Perform after calculating all Qs for all celestials.
    
    :returns: None
    """
    def pushPositionFromQueueIntoCurrent(self):
        self.position = self.positionQueue

    """
    Draw the planet

    :returns: None
    """
    def draw(self):
        self.sphere.move(self.positionQueue.x - self.position.x, self.positionQueue.y - self.position.y)

    def undraw(self):
        self.sphere.undraw()
