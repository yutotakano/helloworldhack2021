import pygame

# required to initialise before any code
pygame.init()

# set up window
DISPLAY = pygame.display.set_mode((600,600))
WHITE = pygame.Color(255, 255, 255)

#Game loop
while True:
    # Get all events currently in que, and handle them accordingly
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.display.quit() # quit the window
                pygame.quit() # quit pygame engine
                exit() # quit code

    # draw white circle
    pygame.draw.circle(DISPLAY, WHITE, (200,50), 30)

    # update game display
    pygame.display.update()