from pygame.locals import QUIT
from renderer      import NDRenderer, Color
import pygame as pg
import numpy  as np
import sys

# Functions
def update():
    rotscale = 4 if export_frames else 1
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

# Globals
size       = 1024, 650
framecount = 0

highlight_cell = True
export_frames  = False

ndims = 5

pg.init()
pg.display.set_caption(f"{ndims}-Cube")

window = pg.display.set_mode(size)
render = NDRenderer(size, window, ndims)

rotSpeed  = np.full(ndims, 1)
points    = render.cube(ndims)

while True:
    framecount += 1

    window.fill(Color.grey)
    update()
    pg.display.update()
    
    # For creating Gifs
    if export_frames:
        pg.image.save(window, f"frames/{framecount}.jpg")

        errormargin = .01
        if render.rotation[0] > np.pi*2 - errormargin and render.rotation[0] < np.pi*2 + errormargin:
            pg.quit()
            sys.exit()

    for e in pg.event.get():
        if e.type == QUIT:
            pg.quit()
            sys.exit()
