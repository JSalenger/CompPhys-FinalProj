from V import V

def tick(forces, mass, velocity: V, position: V, dt):
    """
    Calculates next position based on the sum of forces, mass, previous velocity, position, and delta time

    returns (newPosition, newVelocity)
    """
    acceleration = forces/mass
    velocity += acceleration*dt
    position += velocity*dt

    return (position, velocity)