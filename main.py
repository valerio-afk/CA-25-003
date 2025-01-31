import pygame
from pygame.locals import QUIT
from shape import Shape, MinkowskiDifferenceShape

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Colors
WHITE = pygame.Color((255, 255, 255))
RED = pygame.Color((255, 0, 0))
BLUE = pygame.Color((0, 0, 255))
GREEN = pygame.Color((0,255,0))
BLACK = pygame.Color((0,0,0))

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GJK Algorithm")


# Clock to control the frame rate
clock = pygame.time.Clock()

# Main loop flag
running = True



square = Shape( [(200, 200), (300, 200), (300, 300), (200, 300)], GREEN)
triangle = Shape( [(400, 300), (500, 500), (300, 500)], BLUE)

square.scale(1.5)
triangle.move((400,0))

v1 = pygame.Vector2((2,1)).normalize()/-10
v2 = pygame.Vector2((-1,0)).normalize()/-10

# triangle.move(v*4900)


bg = BLACK


while running:
    dt = clock.tick(120)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Fill the screen with white
    screen.fill(bg)

    m = MinkowskiDifferenceShape(square,triangle,WHITE)


    square.draw(screen)
    triangle.draw(screen)
    triangle.move(v1*dt)
    triangle.rotate(dt/10)
    square.move(v2*dt)

    # Update the display
    pygame.display.flip()

    bg=RED if (triangle in square) else BLACK



# Quit pygame
pygame.quit()
