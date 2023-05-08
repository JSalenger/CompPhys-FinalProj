from Planet import Planet
from typing import List
from V import V
from constants import dt

class Orrery:
    def __init__(self, planets: List[Planet]):
        self.planets = planets
        self.hasBeenAcknowledgedAsDead = False

    def update(self):
        for main_idx, main_planet in enumerate(self.planets):
            net_force = V(0, 0, 0)
            for mini_idx, mini_planet in enumerate(self.planets):
                # for each planet calculate force betweeen them excluding main_planet
                if mini_idx != main_idx:
                    # get vector pointing from main -> mini
                    direction = mini_planet.position - main_planet.position

                    # get magnitude of the force
                    magnitude = (6.6743e-11 * main_planet.mass * mini_planet.mass) / ((main_planet.position - mini_planet.position).m ** 2)

                    # scale create a correct force vector with appropriate direction and magnitude
                    force = direction(magnitude)
                    net_force += force

            # apply net force using verlet's method
            delta_pos = main_planet.velocity * dt + .5 * main_planet.acceleration * dt * dt
            main_planet.delta_pos = delta_pos

            new_position = main_planet.position + delta_pos
            new_velocity = main_planet.velocity + main_planet.acceleration * dt * .5
            new_acceleration = net_force / main_planet.mass
            new_velocity = new_velocity + main_planet.acceleration * dt * .5

            main_planet.setTempVals(new_position, new_velocity, new_acceleration)

        for planet in self.planets:
            planet.pushTempVals()

    def isDead(self) -> bool:
        for main_idx, main_planet in enumerate(self.planets):
            for mini_idx, mini_planet in enumerate(self.planets):
                if main_idx != mini_idx and (main_planet.position - mini_planet.position).m < main_planet.radius + mini_planet.radius:
                    return True
                
                if main_idx != mini_idx and (6.6743e-11 * main_planet.mass * mini_planet.mass) / ((main_planet.position - mini_planet.position).m ** 2) < 1e-13:
                    return True
                
        return False
    
    def draw(self):
        for planet in self.planets:
            planet.draw()