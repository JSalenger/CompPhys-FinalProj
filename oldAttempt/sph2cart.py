from V import V
from math import pi
import math

# # theta = azimuth; phi = incline
# vecs = [
#     V(1, 0, pi/2),
#     V(1, pi, pi/2),
#     V(1,pi/2,pi/2),
#     V(1,-pi/2,pi/2),
#     V(1,0,0),
#     V(1,0,-pi/2),
#     V(1,pi/4,pi/4),
#     V(1,pi/4,3*pi/4),
#     V(1,-pi/4,pi/4),
#     V(1,-pi/4,3*pi/4),
#     V(1,3*pi/4,pi/4),
#     V(1,3*pi/4,pi/4),
#     V(1,-3*pi/4,pi/4),
#     V(1,-3*pi/4,3*pi/4)
# ]

# def sph2cart(v):
#     return V(v.x * math.sin(v.z) * math.cos(v.y), v.x * math.sin(v.z) * math.sin(v.y), v.x * math.cos(v.z))

# print("[", end="")
# for k,v in enumerate(vecs):
#     l = sph2cart(v)
#     print("V(" + str(l.x) + ", " + str(l.y) + ", " + str(l.z) + "),", end ="" )
# print("]")

Vs = [V(1.0, 0.0, 0.0),V(-1.0, 0.0, 0.0),V(0.0, 1.0, 0.0),V(0.0, -1.0, 0.0),V(0.0, 0.0, 1.0),V(-1.0, -0.0, 0.0),V(0.5, 0.5, 0.7071067811865476),V(0.5, 0.5, -0.7071067811865475),V(0.5, -0.5, 0.7071067811865476),V(0.5, -0.5, -0.7071067811865475),V(-0.5, 0.5, 0.7071067811865476),V(-0.5, 0.5, 0.7071067811865476),V(-0.5, -0.5, 0.7071067811865476),V(-0.5, -0.5, -0.7071067811865475)]
for x in Vs:
    print(x.m)