from typing import List
from Orrery import Orrery
from Planet import Planet
from random import random, gauss
from V import V

class GNA: 
    def __init__(self, population_sizes: List[int]):
        self.population_sizes = population_sizes
        self.population: List[Orrery] = []
        self.deathCount = 0 
    

        self.createFirstGeneration()

    def createFirstGeneration(self):
        num_planets = 2
        self.deathCount = 0

        for family in self.population_sizes:
            for _ in range(family):
                # create all new orrery-s
                planets: List[Planet] = []
                for _ in range(num_planets):
                    planets.append(Planet(
                        initialPosition = V(random() * 5 - 2.5, random() * 5 - 2.5, random() * 5 - 2.5),
                        initialVelocity = V(random() * 5 - 2.5, random() * 5 - 2.5, random() * 5 - 2.5),
                        mass = 1,
                        color = V(random() * 255, random() * 255, random() * 255)
                    ))

                self.population.append(Orrery(planets))


    def createNextGeneration(self, sortedPopulation: List[Orrery]):
        num_planets = 2
        self.deathCount = 0 

        tempPopulation: List[Orrery] = []

        for family_number, family_size in enumerate(self.population_sizes[:len(self.population_sizes)]):
            for member in range(family_size):
                parent_orrery = sortedPopulation[family_number]
                planets: List[Planet] = []

                for idx in range(num_planets):
                    planets.append(Planet(
                        initialPosition = V(gauss(parent_orrery.planets[idx].initialPosition.x, .1), gauss(parent_orrery.planets[idx].initialPosition.y, .1), gauss(parent_orrery.planets[idx].initialPosition.z, .1)),
                        initialVelocity = V(gauss(parent_orrery.planets[idx].initialVelocity.x, .1), gauss(parent_orrery.planets[idx].initialVelocity.y, .1), gauss(parent_orrery.planets[idx].initialVelocity.z, .1)),
                        mass = 1,
                        color = parent_orrery.planets[idx].color
                    ))
                
                new_orrery = Orrery(planets)
                tempPopulation.append(new_orrery)
        
        self.population = tempPopulation

    def update(self):
        for orrery in self.population:
            isDead = orrery.isDead()
            if not isDead:
                orrery.update()
            elif isDead and orrery.hasBeenAcknowledgedAsDead == False:
                orrery.hasBeenAcknowledgedAsDead = True
                self.deathCount += 1
            else:
                continue

        if self.deathCount == len(self.population):
            # print stats here
            print("gabagool")
            self.createNextGeneration()

    def draw(self):
        for orrery in self.population:
            orrery.draw()
