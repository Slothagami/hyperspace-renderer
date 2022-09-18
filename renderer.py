from project    import *
from PIL        import Image
from pygifsicle import optimize as optimize_gif
import pygame as pg
import sys
import imageio

# TODO: save gif option in renderer, save directly to gif file, instead of saving frames
    # remove make-gif.py
    # update hypercube-inspector.py

class Color:
    white  = (255, 255, 255)
    dwhite = (150, 150, 150)
    grey   = (32, 32, 32)
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
