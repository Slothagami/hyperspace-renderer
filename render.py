import numpy  as np 
import pygame as pg 
import sys
from pygame.locals import *
from math import sin, cos

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

def transform_matrix(wid, hei):
    return np.identity(max(wid, hei))[:wid,:hei]

# Utility
def rotate_x(a, point):
    rotMatrix = np.identity(len(point))

    if len(point) > 2:
        rotMatrix[1, 1] =  cos(a)
        rotMatrix[2, 1] =  sin(a)
        rotMatrix[1, 2] = -sin(a)
        rotMatrix[2, 2] =  cos(a)

    return np.dot(rotMatrix,  point)

def rotate_n(a, point, axis):
    rotMatrix = np.identity(len(point))

    rotMatrix[   0,    0] =  cos(a)
    rotMatrix[axis,    0] =  sin(a)
    rotMatrix[   0, axis] = -sin(a)
    rotMatrix[axis, axis] =  cos(a)

    return np.dot(rotMatrix, point)

def rotate(point, rot):
    point = rotate_x(rot[0], point)

    for dim in range(1, len(point)):
        point = rotate_n(rot[dim], point, dim)

    return point

def project(point, rot):
    point = rotate(point, rot)
    dims = len(point)
    if dims < 1: raise ValueError("Too few Dimensions")
    scale = 5 ** dims * 1.5

    # project down to 2d
    for dim in reversed(range(2, dims)):
        dist   = 4
        dscale = 1 / (dist - point[-1])
        point  = np.dot(transform_matrix(dim, dim+1) * dscale, point)

    return point * scale
