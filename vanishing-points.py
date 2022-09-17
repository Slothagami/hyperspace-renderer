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
scale = 200

center    = np.array([width, height]) / 2
transform = np.array([[1, 0, 0], [0, 1, 0]])
rotation  = np.array([0, 0, 0], dtype=float)
points    = cube(3)

class c:
    white = (255, 255, 255)
    grey  = (32, 32, 32)
    lgrey = (80, 80, 80)
    black = (0,0,0)

# Functions 
def update():
    # draw horison line
    pg.draw.line(window, c.black, (0, height/2), (width, height/2))

    for point in points:
        # Connect Edges (if two points share enough coordinates)
        for p in points:
            shared = 0
            for pord, ptord in zip(p, point):
                if pord == ptord: shared += 1

            if shared >= 2:
                # Switch to 2d
                p1 = project(point) + center
                p2 = project(p)     + center

                # draw the perspective line
                gradient    = p1 - p2
                gradientVec = gradient * 20
                pg.draw.line(window, c.lgrey, p1, p1 + gradientVec)

                # Draw the Edge itself
                pg.draw.line(window, c.white, p1, p2)

def event(e):
    keys = pg.key.get_pressed()
    rsp = .004

    if keys[K_w]:
        rotation[0] += rsp
    if keys[K_s]:
        rotation[0] -= rsp

    if keys[K_d]:
        rotation[1] += rsp
    if keys[K_a]:
        rotation[1] -= rsp

    if keys[K_o]:
        rotation[2] += rsp
    if keys[K_p]:
        rotation[2] -= rsp


# Utility
def rotateX(a, point):
    rotMatrix = np.array([
        [1,      0,       0],
        [0, cos(a), -sin(a)],
        [0, sin(a),  cos(a)]
    ])

    return np.dot(rotMatrix,  point)

def rotateY(a, point):
    rotMatrix = np.array([
        [ cos(a), 0, sin(a)],
        [      0, 1,      0],
        [-sin(a), 0, cos(a)]
    ])

    return np.dot(rotMatrix,  point)

def rotateZ(a, point):
    rotMatrix = np.array([
        [cos(a), -sin(a), 0],
        [sin(a),  cos(a), 0],
        [     0,       0, 1]
    ])

    return np.dot(rotMatrix, point)

def rotate(rot, point):
    tf = rotateX(rot[0], point)
    tf = rotateY(rot[1], tf)
    tf = rotateZ(rot[2], tf)
    return tf

def project(point):
    global rotation
    point = rotate(rotation, point)

    # scale based on distance
    dist   = 4
    zscale = 1 / (dist - point[2]) # point.z
    return np.dot(transform * zscale, point * scale)

# Pygame Stuff
pg.init()
window = pg.display.set_mode((width, height))

while True:
    window.fill(c.grey)
    update()
    pg.display.update()

    for e in pg.event.get():
        event(e)
        if e.type == QUIT:
            pg.quit()
            sys.exit()