from typing import Any
from V import V
from Celestial import Celestial
from random import random, gauss
from math import floor, sqrt
from graphics import color_rgb

def getRandomSublist(arr, n):
    randomIDXs = [] # the random indexes to put in returned sublist
    
    while len(randomIDXs) < n:
        randomNum = floor(random() * n + .5)
        if randomNum not in randomIDXs:
            randomIDXs.append(randomNum) # TODO: OPTIMIZE LOOP SO THAT IT ONLY RUNS N TIMES

    return [arr[i] for i in randomIDXs]


class Orrery:
    def __init__(self, planets):
        self.planets = planets
        self.tT = 0

        # print("Creating orrery with planets: " + str(planets))

        for k,v in enumerate(self.planets):
            v.id = k
        
        for i in self.planets:
            i.automateDependencies(planets)

        self.dead = False

    def update(self):
        dt = .000001
        for k,v in enumerate(self.planets):
            if k == 0:
                dt = v.putNextPositionInQueue(dt=dt, isFirst = True)
            else:
                v.putNextPositionInQueue(dt=dt)

        for i in self.planets:
            i.draw()

        for i in self.planets:
            i.pushPositionFromQueueIntoCurrent()

        self.tT += dt

    @staticmethod
    def createNew(dt):
        color = color_rgb(int(random() * 255), int(random() * 255), int(random() * 255))

        p1 = Celestial(
            position = V(-1.2237367491640472, -0.5859305104906942, -0.22394447473542467),
            velocity = V(0.28470608817335563, 1.3300667271151392, 1.3778707104641272),
            mass = 1,
            color = color
        )

        p2 = Celestial(
            position = V(-1.9982449565467586, 0.08160775205113513, -1.0274232842417674),
            velocity = V(-0.28470608817335563, -1.3300667271151392, -1.3778707104641272),
            mass = 1,
            color = color
        )

        return Orrery([p1, p2])
    
    @staticmethod
    def createFrom(prevOrrery, _stdDev, color="red"):
        prevOrrery.tT = 0
        newPlanets = []

        prevVelocity = prevOrrery.planets[0].iVelocity    
        newVelocity = V(gauss(prevVelocity.x, .5), gauss(prevVelocity.y, .5), gauss(prevVelocity.z, .5))
        
        newPlanets.append(
            Celestial(
                position = V(gauss(prevOrrery.planets[0].iPosition.x, .5), gauss(prevOrrery.planets[0].iPosition.y, .5), gauss(prevOrrery.planets[0].iPosition.z, .5)),
                velocity = newVelocity,
                mass = 1,
                color = prevOrrery.planets[0].color
            )
        )

        newPlanets.append(
            Celestial(
                position = V(gauss(prevOrrery.planets[1].iPosition.x, .5), gauss(prevOrrery.planets[1].iPosition.y, .5), gauss(prevOrrery.planets[1].iPosition.z, .5)),
                velocity = newVelocity * -1,
                mass = 1,
                color = prevOrrery.planets[1].color
            )
        )

        # for idx,planet in enumerate(prevOrrery.planets):


        #     newPlanets.append(Celestial(
        #         position = V(gauss(planet.iPosition.x, .5), gauss(planet.iPosition.y, .5), gauss(planet.iPosition.z, .5)),
        #         velocity = V(gauss(planet.iVelocity.x, .5), gauss(planet.iVelocity.y, .5), gauss(planet.iVelocity.z, .5)),
        #         mass = 1,
        #         color = planet.color
        #     ))
            

        return Orrery(newPlanets)


    # True means death has ocurred.
    def checkDeath(self):
        for i in self.planets:
            for j in self.planets:
                # check if i collided with j
                if (i.position-j.position).m < i.radius + j.radius and i.id != j.id: 
                    # print("Die from collision")
                    return True
                
                if (i.position-j.position).m > 100 and i.id != j.id: 
                    # print("Die from too far")
                    return True
            # planets can also die when their forces become negligible but thats checked in each planets update func.
            # so we can check if that became true during any loop
            if i.died:
                return True

        return False 
    
    def getChildren(self, lr=.1): 
        # lr = Learning Rate if it is bigger than the values will take bigger jumps per epoch

        # list of vecs all mag. 1 that are equally spaced allowing children to be generated equally across the gradient
        # vecs = [V(1.0, 0.0, 0.0),V(-1.0, 0.0, 0.0),V(0.0, 1.0, 0.0),V(0.0, -1.0, 0.0),V(0.0, 0.0, 1.0),V(-1.0, -0.0, 0.0),V(0.5, 0.5, 0.7071067811865476),V(0.5, 0.5, -0.7071067811865475),V(0.5, -0.5, 0.7071067811865476),V(0.5, -0.5, -0.7071067811865475),V(-0.5, 0.5, 0.7071067811865476),V(-0.5, 0.5, 0.7071067811865476),V(-0.5, -0.5, 0.7071067811865476),V(-0.5, -0.5, -0.7071067811865475)]
        vecs = [V(1., 0., 0.), V(0., 1., 0.), V(0., 0., 1.), V(-1., 0., 0.), V(0., -1., 0.), V(0., 0., -1.)] # decrease number of possibilities for now
        newOrrerys = []
        
        # generate each permutation where Planet 1 moves 1 to the left and P2 move 1 to the left or the right or one up or back etc.
        # so P1 has six different possibilities and each of the P1 have 6 more possibilities    

            # for each planet generate the possibilities of it moving any direction and any of its dependencies moving any direction

        for v1 in getRandomSublist(vecs, 4):
            for v2 in getRandomSublist(vecs, 4):
                for p1 in getRandomSublist(vecs, 4):
                    for p2 in getRandomSublist(vecs, 4):
                        # must create all planets in the inner loop to make sure every instance is unique and planets from one orrery dont belong in others
                        newPlanets = []
                        newColor = V(random() * 255, random() * 255, random() * 255)
                        newPlanets.append(Celestial(self.planets[0].iPosition + p1(lr), self.planets[0].velocity + v1(lr), self.planets[0].mass, color_rgb(int(newColor.x), int(newColor.y), int(newColor.z))))
                        newPlanets.append(Celestial(self.planets[1].iPosition + p2(lr), self.planets[1].velocity + v2(lr), self.planets[1].mass, color_rgb(int(newColor.x), int(newColor.y), int(newColor.z))))
                        newOrrerys.append(Orrery(newPlanets))
                        # print("Created orrery with: " + str(newPlanets))

        print("Created new generation of " + str(len(newOrrerys)) + " orrerys")
        
        return newOrrerys
        
    # calculate similarity between the two orrerys
    def getDistanceFromSelfTo(self, orrery):
        # both orrerys described as a 4d vector
        selfDescription = [self.planets[0].iPosition, self.planets[1].iPosition, self.planets[0].iVelocity, self.planets[1].iVelocity]
        otherDescription = [orrery.planets[0].iPosition, orrery.planets[1].iPosition, orrery.planets[0].iVelocity, orrery.planets[1].iVelocity]

        differences = [(otherDescription[k] - v).m for k, v in enumerate(selfDescription)]
        
        vecLen = sqrt(sum(differences))
        
        # needs to be returned in vector form to be compatible with legacy code
        return V(vecLen, 0, 0)

    def draw(self):
        # bg stuff if I want
        return
    
    def undraw(self):
        for p in self.planets:
            p.undraw()
    
    def getScore(self):
        print(sum(self.planets[0].Gmags) / len(self.planets[0].Gmags))
        return (.5 * sum(self.planets[0].Gmags) / len(self.planets[0].Gmags)) + .5 * self.planets[0].totalDistanceTraveled.m + (.5 * sum(self.planets[1].Gmags) / len(self.planets[0].Gmags)) + .5 * self.planets[1].totalDistanceTraveled.m
    
    def getStats(self):
        return (self.tT, self.planets[0].totalDistanceTraveled.m, sum(self.planets[0].Gmags) / len(self.planets[0].Gmags))

    def __call__(self):
        dead = self.checkDeath()
        if dead and not self.dead:
            self.dead = True
            return True
        elif dead or self.dead:
            return False
        else:
            self.update()
            return False
        
    def undraw(self):
        for p in self.planets:
            p.undraw()