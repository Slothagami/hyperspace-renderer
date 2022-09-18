from pygame.locals import QUIT, KEYDOWN, K_SPACE, K_w, K_a, K_s, K_d
from renderer      import HyperspaceRenderer, Color
import numpy  as np 
import pygame as pg 
import sys

highlight_cell = True

screen_size   = 1024, 650
ndims         = 5
paused        = True

rot3d     = np.zeros(3, dtype=float)

rotSpeed  = np.full(ndims, 1)
rotSpeed[:3] = [0,0,0] # don't spin in the first 3 dims

# Functions 
def update():
    global paused

    if not paused:
        render.rotation += rotSpeed * .003
        
    render.rotation[:3] = rot3d

    for point in points:
        for p in points:
            if render.shared_ordinates(p, point) >= len(point) - 1:
                if highlight_cell and point[-1] != 1:
                    color = Color.orange
                else: color = Color.dwhite

                render.edge(p, point, color)

    # Rotate in 3d
    rotspd = .05
    pressed = pg.key.get_pressed()
    if pressed[K_a]: rot3d[-1] += rotspd
    if pressed[K_d]: rot3d[-1] -= rotspd

    if pressed[K_w]: rot3d[0] += rotspd
    if pressed[K_s]: rot3d[0] -= rotspd

def event(e):
    global paused
    if e.type == KEYDOWN:
        if e.key == K_SPACE: paused = not paused

# Pygame Stuff
pg.init()
pg.display.set_caption(f"{ndims}-Cube")
window = pg.display.set_mode(screen_size)
render = HyperspaceRenderer(screen_size, window, ndims)
points = render.cube(ndims)

while True:
    window.fill(Color.grey)
    update()
    pg.display.update()

    for e in pg.event.get():
        event(e)
        if e.type == QUIT:
            pg.quit()
            sys.exit()
