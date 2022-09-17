from project import *
import pygame as pg

class Color:
    white  = (255, 255, 255)
    dwhite = (150, 150, 150)
    grey   = (32, 32, 32)
    orange = (255, 100, 0)

class NDRenderer:
    def __init__(self, screen_size, window, ndims):
        self.screen_size = screen_size
        self.window = window 
        self.center = np.array(screen_size) / 2
        self.rotation = np.zeros(ndims, dtype=float)
    
    def point(self, point, color, radius=3):
        pg.draw.circle(
            self.window, color, 
            project(point, self.rotation) + self.center, 
            radius
        )

    def edge(self, a, b, color, thickness=2):
        pg.draw.line(
            self.window, color, 
            project(a, self.rotation) + self.center, 
            project(b, self.rotation) + self.center, 
            thickness
        )

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
