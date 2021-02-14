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
        self.font = pygame.font.SysFont(None, 56)
        
        # tile counters
        self.equals_min = 2
        self.equals_max = 6
        self.equals_counter = 0

        self.op_min = 2
        self.op_max = 4
        self.op_counter = 0

        self.none_counter = 0

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
        # If it is a left click and there's a drag going on
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
        # check if it's in the boundaries of the reset button
        elif event.button == 1:
            if (event.pos[0] > 22 and event.pos[0] < 106
            and event.pos[1] > 360 and event.pos[1] < 404):
                self.on_shuffle_click()

    def randomize_board(self):
        self.op_counter = 0
        self.equals_counter = 0
        self.none_counter = 25
        for i, column in enumerate(self.board):
            for j, tile in enumerate(column):
                self.generate_random_tile((i, j))
        list = self.match_exists()
        print(list)
        while(list):
            for position in list:
                print(position)
                self.remove_tile_at_pos(position)
            self.refill_empty_tiles()
            list = self.match_exists()


    def remove_tile_at_pos(self, position):
        tile_to_remove = self.board[position[0]][position[1]]
        if tile_to_remove == None:
            print("NANI, None in remove tile")
        else:
            if tile_to_remove.kind == "op":
                if tile_to_remove.value == "=":
                    self.equals_counter -= 1
                else:
                    self.op_counter -= 1
            self.board[position[0]][position[1]] = None
            self.none_counter += 1

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
        num_weight = 50
        op_weight = 10
        eq_weight = 20
        total_weight = num_weight + op_weight + eq_weight

        rand = random.uniform(0,1)

        if (self.none_counter <= 2) & (self.equals_counter < self.equals_min):
            tile = Tile("equals", "=")
            self.board[pos[0]][pos[1]] = tile
            self.equals_counter += 1

        elif (self.none_counter <= 3) & (self.op_counter < self.op_min):
            opdict = {
                "+": "add",
                "-": "minus"
            }

            tile_value = random.choice(["+", "-"])

            tile = Tile(opdict[tile_value], tile_value)
            self.board[pos[0]][pos[1]] = tile
            self.op_counter += 1

        elif (rand < eq_weight/total_weight) & (self.equals_counter < self.equals_max):
            tile = Tile("equals", "=")
            self.board[pos[0]][pos[1]] = tile
            self.equals_counter += 1

        elif (rand < (eq_weight + op_weight)/total_weight) & (self.op_counter < self.op_max):
            opdict = {
                "+": "add",
                "-": "minus"
            }

            tile_value = random.choice(["+", "-"])

            tile = Tile(opdict[tile_value], tile_value)
            self.board[pos[0]][pos[1]] = tile
            self.op_counter += 1

        else:
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

        self.none_counter -= 1

    def bothNum(self,tile1,tile2): 
        if ((tile1.kind == tile2.kind) and (tile1.kind == "num")):
            return True
        else:
            return False 

    def bothPlusMinus(self,tile1,tile2):
        if (tile2.isPlusMinus() and tile1.isPlusMinus()):
            return True
        else:
            return False

    def lookForEq1(self):
        matchList1 = []
        for i in range(0,5):
            for j in range(1,4):
                if(self.board[i][j].isEqTile()):
                    if(self.bothNum(self.board[i][j-1],self.board[i][j+1])):
                        if int(self.board[i][j+1].value) == int(self.board[i][j-1].value): 
                            matchList1 = matchList1 + [(i,j-1),(i,j),(i,j+1)]
                    
                        elif (j == 1 and self.board[i][3].isPlusMinus() and self.board[i][4].isNumTile()):
                            if int(self.board[i][0].value) == eval(str(self.board[i][2].value)+self.board[i][3].value+str(self.board[i][4].value)):
                                matchList1 = matchList1 + [(i,0),(i,1),(i,2),(i,3),(i,4)]
                    
                        elif (j == 3 and self.board[i][1].isPlusMinus() and self.board[i][0].isNumTile()):
                            if int(self.board[i][4].value) == eval(str(self.board[i][0].value)+self.board[i][1].value+str(self.board[i][2].value)):
                                matchList1 = matchList1 + [(i,0),(i,1),(i,2),(i,3),(i,4)]     
        return matchList1

    def looksForEq2(self):
        matchList2 = []
        for j in range(0,5):
            for i in range(1,4):
                if(self.board[i][j].isEqTile()):
                    if(self.bothNum(self.board[i-1][j],self.board[i+1][j])):
                        if int(self.board[i-1][j].value) == int(self.board[i+1][j].value): 
                            matchList2 = matchList2 + [(i-1,j),(i,j),(i+1,j)]
                    
                        elif (i == 1 and self.board[3][j].isPlusMinus() and self.board[4][j].isNumTile()):
                            if int(self.board[0][j].value) == eval(str(self.board[2][j].value)+self.board[3][j].value+str(self.board[4][j].value)):
                                matchList2 = matchList2 + [(0,j),(1,j),(2,j),(3,j),(4,j)]
                    
                        elif (i == 3 and self.board[1][j].isPlusMinus() and self.board[0][j].isNumTile()):
                            if int(self.board[4][j].value) == eval(str(self.board[0][j].value)+self.board[1][j].value+str(self.board[2][j].value)):
                                matchList2 = matchList2 + [(0,j),(1,j),(2,j),(3,j),(4,j)]      

        return matchList2
    
    def match_exists(self):
        matches1 = self.lookForEq1()
        matches2 = self.looksForEq2()
        matches1 = matches1 + matches2
        netMatches = []
        [netMatches.append(x) for x in matches1 if x not in netMatches]
        match_sound = mixer.Sound('match.wav')
        match_sound.set_volume(0.4)
        match_sound.play()
        return netMatches



    def swap_tiles(self, oldpos, newpos):
        # note that if it crashes because of this, it's because python lists of objects are not lists of references like I thought, sorry.
        swapper = self.board[oldpos[0]][oldpos[1]]
        self.board[oldpos[0]][oldpos[1]] = self.board[newpos[0]][newpos[1]]
        self.board[newpos[0]][newpos[1]] = swapper
    
    def calculate_points(self, points):
        return 1
    
    def on_drag_and_drop(self, oldpos, newpos):
        # called when a tile is dragged and dropped
        print("swapped", oldpos, "with", newpos)
        self.swap_tiles(oldpos, newpos)

        did_enter_loop = False

        # As long as a match exists, handle it
        while tile_positions := self.match_exists():
            did_enter_loop = True

            # find how many points to add
            points = 1 # self.calculate_points(tile_positions)
            self.points += points
            
            # remove the tiles, add new random ones, then add those points
            for position in tile_positions:
                self.remove_tile_at_pos(position)
            self.refill_empty_tiles()

        if not did_enter_loop:
            self.swap_tiles(newpos, oldpos)

    def on_shuffle_click(self):

        if self.remaining_shuffle_count > 0:
            self.randomize_board()
            reshuffle_sound = mixer.Sound('Reshuffle.wav')
            reshuffle_sound.set_volume(0.4)
            reshuffle_sound.play()
            self.remaining_shuffle_count -= 1
        else:
            pass
            
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

        points_text = self.font.render(str(self.remaining_shuffle_count), True, pygame.Color(0, 0, 0))
        self.screen.blit(points_text, (124 - (points_text.get_rect().width / 2), 367))

        points_text = self.font.render(str(self.points), True, pygame.Color(0, 0, 0))
        self.screen.blit(points_text, (300 - (points_text.get_rect().width / 2), 367))

        pygame.display.update()

    def game_over(self):
        # TODO:
        pygame.display.quit()
        pygame.quit()
        exit()