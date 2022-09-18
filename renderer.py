from PIL        import Image
from pygifsicle import optimize as optimize_gif
from math       import sin, cos
import pygame as pg
import numpy  as np
import sys, imageio

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

    depth_scale = 4 ** (dims + 1)
    scale = 1.5

    # project down to 2d
    while len(point) > 2:
        dist   = 4
        dscale = 1 / (dist - point[-1])
        if dscale < 0: return
        point  = point[:-1] * dscale # discard last coordinate

    return point * scale * depth_scale


class Color:
    white  = (255, 255, 255)
    dwhite = (150, 150, 150)
    grey   = (32, 32, 32)
    dgrey   = (16, 16, 16)
    orange = (255, 100, 0)

class HyperspaceRenderer:
    def __init__(self, screen_size, window, ndims, save_to=None, gif_fps=24):
        self.screen_size = screen_size
        self.window      = window 

        self.save_to     = save_to
        self.save_gif    = save_to is not None
        if self.save_gif:
            self.gif = imageio.get_writer(save_to, mode="I", duration=1/gif_fps)

        self.center      = np.array(screen_size) / 2
        self.rotation    = np.zeros(ndims, dtype=float)
    
    def point(self, point, color, radius=3, scale=1):
        point = project(point, self.rotation)
        if point is None: return

        pg.draw.circle(
            self.window, color, 
            point * scale + self.center, 
            radius
        )

    def pixel(self, point, color, scale=1):
        point = project(point, self.rotation)
        if point is None: return

        self.window.set_at(
            (point * scale + self.center).astype(int), 
            color
        )

    def edge(self, a, b, color, thickness=2):
        pg.draw.line(
            self.window, color, 
            project(a, self.rotation) + self.center, 
            project(b, self.rotation) + self.center, 
            thickness
        )

    def save_frame(self):
        if self.save_gif:
            string = pg.image.tostring(self.window, "RGBA")
            image  = Image.frombytes("RGBA", self.screen_size, string)
            self.gif.append_data(np.asarray(image))

            errormargin = .01
            if self.rotation[0] > np.pi*2 - errormargin and self.rotation[0] < np.pi*2 + errormargin:
                self.gif.close()
                optimize_gif(self.save_to)
                pg.quit()
                sys.exit()

    @staticmethod
    def shared_ordinates(a, b):
        shared = 0
        for a_ord, b_ord in zip(a, b):
            if a_ord == b_ord: shared += 1

        return shared

    @staticmethod
    def cube(dimensions):
        verticies = []
        for i in range(2 ** dimensions):
            binary = bin(i)[2:]
            binary = binary.rjust(dimensions, "0")
            binary = [int(x) for x in binary]

            vertex = [(x - .5) * 2 for x in binary]
            verticies.append(vertex)
        return np.array(verticies)
