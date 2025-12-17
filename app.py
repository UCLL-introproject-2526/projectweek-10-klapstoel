print('Hello world!')

import pygame 
pygame.init()

import pygame


# Initialize Pygame
pygame.init()

# Tuple representing width and height in pixels
screen_size = (1024, 768)

# Create window with given size
pygame.display.set_mode(screen_size)

x = int(input("Please enter an integer: "))
if x < 0:
    x = 0
    print('Negative changed to zero')
elif x == 0:
    print('Zero')
elif x == 1:
    print('Single')
else:
    print('More')

    from pygame.display import flip

# Copying back buffer to front buffer
flip()  # Instead of pygame.display.flip()