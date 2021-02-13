import pygame
import random
from tile import Tile
from pygame import mixer

class Game:

    def __init__(self):
        pygame.init()
        self.board = [[None for i in range(5)] for i in range(5)]
        self.screen = pygame.display.set_mode((350, 435))
        self.points = 0
        self.currently_dragging = None
        self.dragging_offset = None
        self.remaining_shuffle_count = 3

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()  # quit the window
                pygame.quit()  # quit pygame engine
                exit()  # quit code

            # on tiles swapped: game.on_drag_and_drop(oldpos, newpos)
            # on shuffle button click: game.on_shuffle_click 
            # on mouse down, if touching any of the tiles, then set 
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.on_mouse_down(event)
            if event.type == pygame.MOUSEBUTTONUP:
                self.on_mouse_up(event)

    # Handle on mouse down
    def on_mouse_down(self, event):
        # If it is a left click
        if event.button == 1:
            self.currently_dragging = None

            # Loop through all tiles, and check if the click is on one of them
            # If so, then set self.currently_dragging to a tuple of indices
            for i, column in enumerate(self.board):
                for j, tile in enumerate(column):
                    if (event.pos[0] < (i + 1)*64 + 15 and event.pos[0] > i*64 + 15
                    and event.pos[1] < (j + 1)*64 + 15 and event.pos[1] > j*64 + 15):
                        self.currently_dragging = (i, j)
                        break
    
    def on_mouse_up(self, event):
        if event.button == 1 and self.currently_dragging:
            # check where mouse was lifted, similar to checking where it was pressed down
            for i, column in enumerate(self.board):
                for j, tile in enumerate(column):
                    if (event.pos[0] < (i + 1)*64 + 15 and event.pos[0] > i*64 + 15
                    and event.pos[1] < (j + 1)*64 + 15 and event.pos[1] > j*64 + 15
                    and (
                        abs(i - self.currently_dragging[0]) == 1 or
                        abs(j - self.currently_dragging[1]) == 1
                    )):
                        self.on_drag_and_drop(self.currently_dragging, (i, j))
                        break
    

    def randomize_board(self):
        # TODO, update self.board in here

        pass
    
    def remove_tile_at_pos(self, positions):
        self.board.pop([positions[0],positions[1]])
        self.board.insert([positions[0],positions[1]])
        # honestly not sure if this is how it works hopefully i got this right O.O
        pass

    def refill_empty_tiles(self):
        # TODO: fill all empty tiles with random ones
        pass

    def match_exists(self):
        # TODO: finish
        # return None if no match
        # return list of tile (x,y) positions if match found
        # only returns the first match found
        pass

    def swap_tiles(self, oldpos, newpos):
        # note that if it crashes because of this, it's because python lists of objects are not lists of references like I thought, sorry.
        swapper = self.board[oldpos[0], oldpos[1]]
        self.board[oldpos[0], oldpos[1]] = self.board[newpos[0], newpos[1]]
        self.board[newpos[0], newpos[1]] = swapper
        
    def on_drag_and_drop(self, oldpos, newpos):
        # called when a tile is dragged and dropped
        print("swapped", oldpos, "with", newpos)
        self.swap_tiles(oldpos, newpos)

        did_enter_loop = False

        # As long as a match exists, handle it
        while tile_positions := self.match_exists():
            did_enter_loop = True

            # find how many points to add
            points = self.calculate_points(tile_positions)
            self.points += points
            
            # remove the tiles, add new random ones, then add those points
            self.remove_tiles_at_pos(tile_positions)
            self.refill_empty_tiles()

        if not did_enter_loop:
            self.swap_tiles(newpos, oldpos)

    def on_shuffle_click(self):

        if self.remaining_shuffle_count <= 0:
            self.game_over()
        else:
            self.randomize_board()
            self.remaining_shuffle_count -= 1
            
    def update_display(self):
        # screen.draw and stuff
        bg = pygame.image.load("bg.png")
        bg = pygame.transform.scale(bg, (350, 435))
        self.screen.blit(bg, (0, 0))
    
        for i, tiles in enumerate(self.board):
            for j, tile in enumerate(tiles):
                if tile is None:
                    continue
                image = pygame.image.load(tile.get_image_path())
                self.screen.blit(image, (i*64+15+tile.offset_x, j*64+15+tile.offset_y))

        pygame.display.update()

    def game_over(self):
        # TODO:
        self.pygame.quit()
        pass