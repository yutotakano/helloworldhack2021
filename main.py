import pygame
from game import Game

# required to initialise before any code
pygame.init()

# set up window
screen = pygame.display.set_mode((640, 640))
screen.fill("white")

game = Game(pygame) 
game.randomize_board()
game.update_display()

# Game loop
while True:
    # Get all events currently in que, and handle them accordingly
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()  # quit the window
            pygame.quit()  # quit pygame engine
            exit()  # quit code

        # on tiles swapped: game.on_drag_and_drop(oldpos, newpos)
        # on shuffle button click: game.on_shuffle_click 
       

    # Refresh screen
    game.update_display()
