from pygame.locals import QUIT
from renderer      import HyperspaceRenderer, Color
import pygame as pg
import numpy  as np
import sys

# Functions
def update():
    rotscale = 4 if render.save_gif else 1
    render.rotation += rotSpeed * .003 * rotscale

    for point in points:
        for p in points:
            # Connect Edges (if two points share enough coordinates)
            if render.shared_ordinates(p, point) >= len(point) - 1:
                # Handle Color Settings
                if highlight_cell and point[-1] != 1:
                    color = Color.orange
                else: color = Color.dwhite

                render.edge(p, point, color)

    render.save_frame()

# Globals
size           = 1024, 650
highlight_cell = True
ndims          = 5

pg.init()
pg.display.set_caption(f"{ndims}-Cube")

window = pg.display.set_mode(size)
render = HyperspaceRenderer(size, window, ndims, f"gifs/{ndims}-Cube.gif")

rotSpeed  = np.full(ndims, 1)
points    = render.cube(ndims)

while True:
    window.fill(Color.grey)
    update()
    pg.display.update()

    for e in pg.event.get():
        if e.type == QUIT:
            pg.quit()
            sys.exit()
