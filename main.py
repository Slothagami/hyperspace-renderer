import pygame as pg
from render import *

# Functions
def update():
    global rotation

    rotscale = 1
    if export_frames: rotscale = 4

    rotation += rotSpeed * .003 * rotscale

    for point in points:
        # Connect Edges (if two points share enough coordinates)
        for p in points:
            shared = 0
            for pord, ptord in zip(p, point):
                if pord == ptord: shared += 1

            if shared >= len(point) - 1:
                if highlight_cell:
                    color = c.dwhite if point[-1] == 1 else c.orange
                else:
                    color = c.white

                pg.draw.line(
                    window, color, 
                    project(point, rotation) + center, 
                    project(p, rotation) + center, 
                    2
                )

# Pygame Stuff
class c:
    white  = (255, 255, 255)
    dwhite = (150, 150, 150)
    grey   = (32, 32, 32)
    orange = (255, 100, 0)

# Globals
width, height = 1024, 650
center        = np.array([width, height]) / 2
framecount    = 0

n = 5
rotation  = np.zeros(n, dtype=float)
rotSpeed  = np.full(n, 1)
points    = cube(n)

pg.init()
pg.display.set_caption(f"{n}-Cube")
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
