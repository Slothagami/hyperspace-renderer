import numpy  as np 
import pygame as pg 
import sys
from pygame.locals import *
from math import sin, cos

def cube(dimensions):
    c = []
    for i in range(2 ** dimensions):
        binary = bin(i)[2:]
        binary = binary.rjust(dimensions, "0")
        binary = [int(x) for x in binary]

        vertex = [(x - .5) * 2 for x in binary]
        c.append(vertex)
    return np.array(c)

# Globals
width, height = 1024, 650
scale = 1200
dims = 4

center      = np.array([width, height]) / 2
transform2d = np.array([[1, 0, 0], [0, 1, 0]])
transform3d = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])
rotation    = np.zeros(dims, dtype=float)
rotSpeed    = np.array([1, 1, 1, 1])#np.random.randn(4) * np.array([.01, 0, 0, 5])
points      = cube(dims)

class c:
    white = (255, 255, 255)
    grey  = (32, 32, 32)

# Functions 
def update():
    global rotation
    rotation += rotSpeed * .0009

    for point in points:
        # Draw Points
        # projection = project(point)
        # pg.draw.circle(window, c.white, projection + center, 3)

        # Connect Edges (if two points share enough coordinates)
        for p in points:
            shared = 0
            for pord, ptord in zip(p, point):
                if pord == ptord: shared += 1

            if shared >= dims -1:
                pg.draw.line(window, c.white, project(point) + center, project(p) + center)

# Utility
def rotateX(a, point):
    rotMatrix = np.array([
        [1,      0,       0, 0],
        [0, cos(a), -sin(a), 0],
        [0, sin(a),  cos(a), 0],
        [0,      0,       0, 1]
    ])

    return np.dot(rotMatrix,  point)

def rotateY(a, point):
    rotMatrix = np.array([
        [ cos(a), 0, sin(a), 0],
        [      0, 1,      0, 0],
        [-sin(a), 0, cos(a), 0],
        [      0, 0,      0, 1]
    ])

    return np.dot(rotMatrix,  point)

def rotateZ(a, point):
    rotMatrix = np.array([
        [cos(a), -sin(a), 0, 0],
        [sin(a),  cos(a), 0, 0],
        [     0,       0, 1, 0],
        [     0,       0, 0, 1],
    ])

    return np.dot(rotMatrix, point)

def rotateW(a, point):
    # rotMatrix = np.array([
    #     [1, 0,      0,       0],
    #     [0, 1,      0,       0],
    #     [0, 0, cos(a), -sin(a)],
    #     [0, 0, sin(a),  cos(a)],
    # ])
    rotMatrix = np.array([
        [cos(a), 0, 0, -sin(a)],
        [     0, 1, 0,       0],
        [     0, 0, 1,       0],
        [sin(a), 0, 0,  cos(a)],
    ])

    return np.dot(rotMatrix, point)

def rotate(rot, point):
    tf = rotateX(rot[0], point)
    tf = rotateY(rot[1], tf)
    tf = rotateZ(rot[2], tf)
    tf = rotateW(rot[3], tf)
    return tf

def project(point):
    global rotation
    # Transform in 4d
    point = rotate(rotation, point)

    # scale based on distance (4d perspective)
    dist   = 4
    wscale = 1 / (dist - point[3]) # point.w (4th dim)

    # project to 3d
    point  = np.dot(transform3d * wscale, point)

    # 3d perspective
    dist   = 4
    zscale = 1 / (dist - point[2]) 

    return np.dot(transform2d * zscale, point * scale)

# Pygame Stuff
pg.init()
window = pg.display.set_mode((width, height))

while True:
    window.fill(c.grey)
    update()
    pg.display.update()

    for e in pg.event.get():
        if e.type == QUIT:
            pg.quit()
            sys.exit()