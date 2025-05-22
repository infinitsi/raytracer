### Ray tracer

# libs
import pygame
import cProfile
import os
# modules
from rtweekend import *
from hittable import *
from hittable_list import *
from sphere import *
from camera import *


# pygame setup
pygame.init()
screen = pygame.display.set_mode((720, 360))
main_dir = os.path.split(os.path.abspath(__file__))[0]
clock = pygame.time.Clock()
running = True


# load image
def load_image(file):
    file = os.path.join(main_dir, "images", file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit(f'Could not load image "{file}" {pg.get_error()}')
    return surface.convert()

# world
world = hittable_list()
material_ground = lambertian((.8,.8,0))
material_center = lambertian((.1,.2,.5))
material_left   = dielectric(1.5)
material_bubble = dielectric(1/1.5)
material_right  = metal((1,.7,0.11),0.1)

world.add(sphere(( 0, -100.5,    1),  100, material_ground))
world.add(sphere(( 0,      0, -1.2),  0.5, material_center))
world.add(sphere((-1,      0,   -1),  0.5, material_left))
world.add(sphere((-1,      0,   -1),  0.4, material_bubble))
world.add(sphere(( 1,      0,   -1),  0.5, material_right))

cam = camera()
# settings
cam.screenWidth = screen.get_width()
cam.screenHeight = screen.get_height()

cam.lookfrom = Vector3(-1,0,0)
cam.lookat = Vector3(0,0,-1)

cam.fov = 90
cam.samples_per_pixel = 2
cam.max_depth = 50
# sky, black, skyBox
cam.skyMode = 'skyBox'
skyBox = load_image('Surreal-sunset.png')
cam.skyBox = skyBox

# render
# cam.render(world,screen)
cProfile.run('cam.render(world,screen)')









# loop

while running:
    # poll for events
    # QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    # screen.fill("cyan")

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
