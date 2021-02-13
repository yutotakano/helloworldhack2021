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
        for i, column in enumerate(self.board):
            for j, tile in enumerate(column):
                self.generate_random_tile(i, j)

    
    def remove_tile_at_pos(self, positions):
        self.board.pop([positions[0][positions[1]]])
        self.board.insert([positions[0][positions[1]]])

    def refill_empty_tiles(self):
        # TODO: fill all empty tiles with random ones
        # only refill tiles from top, first move all tiles down
        while(self.empty_checker()):
            for i in range(5):
                for j in range(5):
                    if self.board[i][j] == None:
                        if j == 0:
                            self.generate_random_tile((i, j))
                        else:
                            self.swap_tiles((i, j-1), (i, j))

    # returns whether there are any None tile values inside board
    def empty_checker(self):
        for column in self.board:
            for tile in column:
                if tile == None:
                    return True
        return False

    def generate_random_tile(self, pos):
        #TODO: fill with random tile
        num_weight = 50
        op_weight = 20
        eq_weight = 20
        total_weight = num_weight + op_weight + eq_weight

        rand = random.uniform(0,1)

        if rand < num_weight/total_weight:
            numdict = {
                1: "one",
                2: "two",
                3: "three",
                4: "four",
                5: "five"
            }

            tile_number = random.randint(1,5)

            tile = Tile(numdict[tile_number], tile_number)
            self.board[pos[0]][pos[1]] = tile

        elif rand < (num_weight + op_weight)/total_weight:
            opdict = {
                "+": "plus",
                "-": "minus"
            }

            tile_value = random.choice(["+", "-"])

            tile = Tile(opdict[tile_value], tile_value)
            self.board[pos[0]][pos[1]] = tile

        else:
            tile = Tile("equals", "=")
            self.board[pos[0]][pos[1]] = tile

    def match_exists(self):
        # TODO: finish
        # return None if no match
        # return list of tile (x,y) positions if match found
        # only returns the first match found
        match_sound = mixer.Sound('match.wav')
        match_sound.play()
        pass

    def swap_tiles(self, oldpos, newpos):
        # note that if it crashes because of this, it's because python lists of objects are not lists of references like I thought, sorry.
        swapper = self.board[oldpos[0]][oldpos[1]]
        self.board[oldpos[0]][oldpos[1]] = self.board[newpos[0]][newpos[1]]
        self.board[newpos[0]][newpos[1]] = swapper
        
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
            reshuffle_sound = mixer.Sound('Reshuffle.wav')
            reshuffle_sound.play()
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