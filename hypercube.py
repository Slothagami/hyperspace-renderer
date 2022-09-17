import numpy  as np 
import pygame as pg 
import sys
from pygame.locals import *
from math import sin, cos

"""
    Generates a 3d projection of a n-dimensional hypercube
    Change the variable to see different dimensions

    Based on: youtu.be/p4Iz0XJY-Qk and youtu.be/XE3YDVdQSPo
    Created on September 15, 2021
"""
hypercube_dimensions = 3
highlight_cell = True
export_frames  = False

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
scale = 5 ** dims * 1.5
framecount = 0

center = np.array([width, height]) / 2

# Generate transform matrices
# make the biggest one, and slice it for the smaller ones
transform = transformMatrix(dims-1, dims)
rotation  = np.zeros(dims, dtype=float)
rotSpeed  = np.full(dims, 1)
points    = cube(dims)

class c:
    white  = (255, 255, 255)
    dwhite = (150, 150, 150)
    grey   = (32, 32, 32)
    orange = (255, 100, 0)

# Functions 
def update():
    global rotation

    rotscale = 1
    if export_frames: rotscale = 4

    rotation += rotSpeed * .003 * rotscale

    for point in points:
        # Draw Points
        # projection = project(point)
        # pg.draw.circle(window, c.white, projection + center, 3)

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

                pg.draw.line(window, color, project(point) + center, project(p) + center, 2)

# Utility
def rotateX(a, point):
    rotMatrix = transformMatrix(dims, dims)

    if dims > 2:
        rotMatrix[1, 1] =  cos(a)
        rotMatrix[2, 1] =  sin(a)
        rotMatrix[1, 2] = -sin(a)
        rotMatrix[2, 2] =  cos(a)

    return np.dot(rotMatrix,  point)

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

def project(point):
    global rotation

    # rotate in highest dimension
    point = rotate(rotation, point)

    # project down to 2d
    for dim in reversed(range(2, dims)):
        dist   = 4
        dscale = 1 / (dist - point[-1])
        point  = np.dot(transform[:dim, :dim+1] * dscale, point)

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
    
    # For creating Gifs
    if export_frames:
        pg.image.save(window, f"frames/{framecount}.jpg")

        errormargin = .01
        if rotation[0] > np.pi*2 - errormargin and rotation[0] < np.pi*2 + errormargin:
            pg.quit()
            sys.exit()

    for e in pg.event.get():
        if e.type == QUIT:
            pg.quit()
            sys.exit()
