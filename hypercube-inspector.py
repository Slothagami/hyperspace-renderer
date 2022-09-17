import numpy  as np 
import pygame as pg 
import sys
from pygame.locals import *
from math import sin, cos, hypot

"""
    Generates a 3d projection of a n-dimensional hypercube
    and lets you inspect it in 3d
    Change the variable to see different dimensions
"""

hypercube_dimensions = 4
highlight_cell = True

def cube(dimensions):
    c = []
    for i in range(2 ** dimensions):
        binary = bin(i)[2:]
        binary = binary.rjust(dimensions, "0")
        binary = [int(x) for x in binary]

        vertex = [(x - .5) * 2 for x in binary]
        c.append(vertex)
    return np.array(c)

def transformMatrix(wid, hei):
    transform = np.zeros((wid, hei))
    for i, row in enumerate(transform):
        row[i] = 1

    return transform

if hypercube_dimensions < 1: raise ValueError("Too few hypercube dimensions")

# Globals
width, height = 1024, 650
dims = hypercube_dimensions # dimensions of the cube
# there are 2^n verticies in an n dimensional cube
scale = 4.3 ** dims
framecount = 0
paused = True

center = np.array([width, height]) / 2

# Generate transform matrices
# make the biggest one, and slice it for the smaller ones
transform = transformMatrix(dims-1, dims)

rotation  = np.zeros(dims, dtype=float)
rot3d     = np.zeros(3, dtype=float)

rotSpeed  = np.full(dims, 1)
rotSpeed[:3] = [0,0,0] # dont spin in the first 3 dims
print(rotSpeed)

points    = cube(dims)

pmouse = np.array([0,0])
mouse  = np.array([0,0])

class c:
    white  = (255, 255, 255)
    dwhite = (150, 150, 150)
    grey   = (32, 32, 32)
    orange = (255, 100, 0)

# Functions 
def update():
    global rotation, paused

    if not paused:
        rotation += rotSpeed * .003

    for point in points:
        # Connect Edges (if two points share enough coordinates)
        for p in points:
            shared = 0
            for pord, ptord in zip(p, point):
                if pord == ptord: shared += 1

            if shared >= dims - 1:
                if highlight_cell:
                    color = c.dwhite if point[-1] == 1 else c.orange
                else:
                    color = c.white

                pg.draw.line(window, color, project(point) + center, project(p) + center)

def event(e):
    global paused, pmouse, mouse

    mouse = np.array(pg.mouse.get_pos(), dtype=float)

    if pg.mouse.get_pressed()[0]:
        rot3d[:2] += np.flip(mouse - pmouse) * .0023

    pmouse = mouse

    if e.type == KEYDOWN:
        if e.key == K_r: paused = not paused

# Utility
def rotateX(a, point, d3=False):
    if d3:
        rotMatrix = transformMatrix(3, 3)
    else: rotMatrix = transformMatrix(dims, dims)

    if dims > 2:
        rotMatrix[1, 1] =  cos(a)
        rotMatrix[2, 1] =  sin(a)
        rotMatrix[1, 2] = -sin(a)
        rotMatrix[2, 2] =  cos(a)

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

def rotateN(a, point, axis):
    rotMatrix = transformMatrix(dims, dims)

    rotMatrix[   0,    0] =  cos(a)
    rotMatrix[axis,    0] =  sin(a)
    rotMatrix[   0, axis] = -sin(a)
    rotMatrix[axis, axis] =  cos(a)

    return np.dot(rotMatrix, point)

def rotate(rot, point):
    point = rotateX(rot[0], point)

    for dim in range(1, dims):
        point = rotateN(rot[dim], point, dim)

    return point

def rotate3d(rot, point):
    tf = rotateX(rot[0], point, d3=True)
    tf = rotateY(rot[1], tf)
    tf = rotateZ(rot[2], tf)
    return tf

def project(point):
    global rotation, rot3d

    # rotate in highest dimension
    point = rotate(rotation, point)

    # project down to 2d
    for dim in reversed(range(2, dims)):
        dist   = 3
        dscale = 1 / (dist - point[-1])
        point  = np.dot(transform[:dim, :dim+1] * dscale, point)

        if dim == 3: # apply rot3d
            point = rotate3d(rot3d, point)

    return point * scale

# Pygame Stuff
pg.init()
pg.display.set_caption(f"{dims}-Cube")
window = pg.display.set_mode((width, height))

while True:
    framecount += 1

    window.fill(c.grey)
    update()
    pg.display.update()

    for e in pg.event.get():
        event(e)
        if e.type == QUIT:
            pg.quit()
            sys.exit()