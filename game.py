import pygame
import random
from tile import Tile
from pygame import mixer

class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Arithmetic Bejeweled')
        self.board = [[None for i in range(5)] for i in range(5)]
        self.screen = pygame.display.set_mode((350, 435))
        self.points = 0
        self.currently_dragging = None
        self.drag_origin = None
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
            if event.type == pygame.MOUSEMOTION:
                self.on_mouse_move(event)

    # Handle on mouse down
    def on_mouse_down(self, event):
        # If it is a left click
        if event.button == 1:
            # Loop through all tiles, and check if the click is on one of them
            # If so, then set self.currently_dragging to a tuple of indices
            for i, column in enumerate(self.board):
                for j, tile in enumerate(column):
                    if (event.pos[0] < (i + 1)*64 + 15 and event.pos[0] > i*64 + 15
                    and event.pos[1] < (j + 1)*64 + 15 and event.pos[1] > j*64 + 15):
                        self.currently_dragging = (i, j)
                        self.drag_origin = (event.pos[0], event.pos[1])
                        break
    
    def reset_all_offsets(self):
        for i, column in enumerate(self.board):
            for j, tile in enumerate(column):
                # snap back to default pos
                tile.offset_x = 0
                tile.offset_y = 0

    def on_mouse_up(self, event):
        # If it is a left click and there's a drag going on
        if event.button == 1 and self.currently_dragging:
            # check where mouse was lifted, similar to checking where it was pressed down
            for i, column in enumerate(self.board):
                for j, tile in enumerate(column):
                    # snap back to default pos
                    self.reset_all_offsets()

                    if (event.pos[0] < (i + 1)*64 + 15 and event.pos[0] > i*64 + 15
                    and event.pos[1] < (j + 1)*64 + 15 and event.pos[1] > j*64 + 15
                    and (
                        (abs(i - self.currently_dragging[0]) == 1 and abs(j - self.currently_dragging[1]) == 0)
                     or (abs(i - self.currently_dragging[0]) == 0 and abs(j - self.currently_dragging[1]) == 1)
                     or (abs(i - self.currently_dragging[0]) == 1 and abs(j - self.currently_dragging[1]) == 1)
                    )):
                        self.on_drag_and_drop(self.currently_dragging, (i, j))
                        break
        # check if it's in the boundaries of the reset button
        elif event.button == 1:
            if (event.pos[0] > 22 and event.pos[0] < 106
            and event.pos[1] > 360 and event.pos[1] < 404):
                self.on_shuffle_click()
        
        self.currently_dragging = None
        self.drag_origin = None
    
    def on_mouse_move(self, event):
        if self.currently_dragging:
            began_x, began_y = self.drag_origin
            
            mouse_offset_x = began_x - (self.currently_dragging[0]*64+15)
            mouse_offset_y = began_y - (self.currently_dragging[1]*64+15)

            h_offset = min(64, max(-64, event.pos[0] - (self.currently_dragging[0]*64+15) - mouse_offset_x))
            v_offset = min(64, max(-64, event.pos[1] - (self.currently_dragging[1]*64+15) - mouse_offset_y))

            if (event.pos[0] - began_x) > 30 and (event.pos[1] - began_y) > 30:
                self.dragging_direction = "downright"
                offset = max(h_offset, v_offset)
                self.board[self.currently_dragging[0]][self.currently_dragging[1]].offset_x = offset
                self.board[self.currently_dragging[0]][self.currently_dragging[1]].offset_y = offset
            
            elif (event.pos[0] - began_x) > 30 and (event.pos[1] - began_y) < -30:
                self.dragging_direction = "upright"
                offset = max(h_offset, v_offset)
                self.board[self.currently_dragging[0]][self.currently_dragging[1]].offset_x = offset
                self.board[self.currently_dragging[0]][self.currently_dragging[1]].offset_y = -offset
    
            elif (event.pos[0] - began_x) < -30 and (event.pos[1] - began_y) > 30:
                self.dragging_direction = "downleft"
                offset = max(h_offset, v_offset)
                self.board[self.currently_dragging[0]][self.currently_dragging[1]].offset_x = -offset
                self.board[self.currently_dragging[0]][self.currently_dragging[1]].offset_y = offset
            
            elif (event.pos[0] - began_x) < -30 and (event.pos[1] - began_y) < -30:
                self.dragging_direction = "upleft"
                offset = max(h_offset, v_offset)
                self.board[self.currently_dragging[0]][self.currently_dragging[1]].offset_x = offset
                self.board[self.currently_dragging[0]][self.currently_dragging[1]].offset_y = offset
    
            elif (event.pos[0] - began_x) > 10:
                self.dragging_direction = "right"
                self.board[self.currently_dragging[0]][self.currently_dragging[1]].offset_x = min(64, max(-64, event.pos[0] - (self.currently_dragging[0]*64+15) - mouse_offset_x))
                self.board[self.currently_dragging[0]][self.currently_dragging[1]].offset_y = 0

            elif (event.pos[0] - began_x) < -10:
                self.dragging_direction = "left"
                self.board[self.currently_dragging[0]][self.currently_dragging[1]].offset_x = min(64, max(-64, event.pos[0] - (self.currently_dragging[0]*64+15) - mouse_offset_x))
                self.board[self.currently_dragging[0]][self.currently_dragging[1]].offset_y = 0

            elif (event.pos[1] - began_y) > 10:
                self.dragging_direction = "down"
                self.board[self.currently_dragging[0]][self.currently_dragging[1]].offset_x = 0
                self.board[self.currently_dragging[0]][self.currently_dragging[1]].offset_y = min(64, max(-64, event.pos[1] - (self.currently_dragging[1]*64+15) - mouse_offset_y))

            elif (event.pos[1] - began_y) < -10:
                self.dragging_direction = "up"
                self.board[self.currently_dragging[0]][self.currently_dragging[1]].offset_x = 0
                self.board[self.currently_dragging[0]][self.currently_dragging[1]].offset_y = min(64, max(-64, event.pos[1] - (self.currently_dragging[1]*64+15) - mouse_offset_y))


    def randomize_board(self):
        self.op_counter = 0
        self.equals_counter = 0
        self.none_counter = 25
        for i, column in enumerate(self.board):
            for j, tile in enumerate(column):
                self.generate_random_tile((i, j))
        
        while list := self.match_exists():
            match_sound = mixer.Sound("assets/match.wav")
            match_sound.set_volume(0.1)
            match_sound.play()

            self.points += self.calculate_points(list)

            for position in list:
                self.remove_tile_at_pos(position)
            
            self.refill_empty_tiles()

    def initialize_demo1(self):
        self.board = [
            [Tile("one", 1), Tile("add", "+"), Tile("two", 2), Tile("equals", "="), Tile("one", 1)],
            [Tile("four", 4), Tile("equals", "="), Tile("two", 2), Tile("four", 4), Tile("three", 3)],
            [Tile("two", 2), Tile("one", 1), Tile("five", 5), Tile("add", "+"), Tile("minus", "-")],
            [Tile("one", 1), Tile("three", 3), Tile("equals", "="), Tile("four", 4), Tile("three", 3)],
            [Tile("minus", "-"), Tile("four", 4), Tile("three", 3), Tile("equals", "="), Tile("add", "+")],
        ]

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
            for i in range(5):
                tile_to_remove.next_poof()
                self.update_display()
                pygame.time.delay(30)

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
        if (tile2.isOpTile() and tile1.isOpTile()):
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
                    
                        elif (j == 1 and self.board[i][3].isOpTile() and self.board[i][4].isNumTile()):
                            if int(self.board[i][0].value) == eval(str(self.board[i][2].value)+self.board[i][3].value+str(self.board[i][4].value)):
                                matchList1 = matchList1 + [(i,0),(i,1),(i,2),(i,3),(i,4)]
                    
                        elif (j == 3 and self.board[i][1].isOpTile() and self.board[i][0].isNumTile()):
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
                    
                        elif (i == 1 and self.board[3][j].isOpTile() and self.board[4][j].isNumTile()):
                            if int(self.board[0][j].value) == eval(str(self.board[2][j].value)+self.board[3][j].value+str(self.board[4][j].value)):
                                matchList2 = matchList2 + [(0,j),(1,j),(2,j),(3,j),(4,j)]
                    
                        elif (i == 3 and self.board[1][j].isOpTile() and self.board[0][j].isNumTile()):
                            if int(self.board[4][j].value) == eval(str(self.board[0][j].value)+self.board[1][j].value+str(self.board[2][j].value)):
                                matchList2 = matchList2 + [(0,j),(1,j),(2,j),(3,j),(4,j)]      

        return matchList2
    
    def match_exists(self):
        matches1 = self.lookForEq1()
        matches2 = self.looksForEq2()
        matches1 = matches1 + matches2
        netMatches = []
        [netMatches.append(x) for x in matches1 if x not in netMatches]
        return netMatches



    def swap_tiles(self, oldpos, newpos):
        # note that if it crashes because of this, it's because python lists of objects are not lists of references like I thought, sorry.
        swapper = self.board[oldpos[0]][oldpos[1]]
        self.board[oldpos[0]][oldpos[1]] = self.board[newpos[0]][newpos[1]]
        self.board[newpos[0]][newpos[1]] = swapper
    
    def calculate_points(self, points):
        if len(points) >= 5:
            return 5 * len(points)
        else:
            return len(points)
    
    def on_drag_and_drop(self, oldpos, newpos):
        # called when a tile is dragged and dropped
        # print("swapped", oldpos, "with", newpos)
        self.swap_tiles(oldpos, newpos)

        move_sound = mixer.Sound("assets/move.wav")
        move_sound.set_volume(0.8)
        move_sound.play()

        did_enter_loop = False

        # As long as a match exists, handle it
        while tile_positions := self.match_exists():
            did_enter_loop = True
            
            match_sound = mixer.Sound("assets/match.wav")
            match_sound.set_volume(0.1)
            match_sound.play()

            # find how many points to add
            points = self.calculate_points(tile_positions)
            self.points += points
            
            # remove the tiles
            for position in tile_positions:
                self.remove_tile_at_pos(position)
            self.refill_empty_tiles()

        if not did_enter_loop:
            self.swap_tiles(newpos, oldpos)

    def on_shuffle_click(self):

        if self.remaining_shuffle_count > 0:
            self.randomize_board()
            reshuffle_sound = mixer.Sound("assets/Reshuffle.wav")
            reshuffle_sound.set_volume(0.4)
            reshuffle_sound.play()
            self.remaining_shuffle_count -= 1
        else:
            pass
            
    def update_display(self):
        # screen.draw and stuff
        bg = pygame.image.load("assets/bg.png")
        bg = pygame.transform.scale(bg, (350, 435))
        self.screen.blit(bg, (0, 0))

        draw_above = []
    
        for i, tiles in enumerate(self.board):
            for j, tile in enumerate(tiles):
                if tile is None:
                    continue
                image = pygame.image.load(tile.get_image_path())
                if tile.poof_sprite != 0:
                    image = pygame.image.load(tile.get_poof_path())
                    image = pygame.transform.scale(image, (64, 64))

                if tile.offset_x or tile.offset_y:
                    image = pygame.transform.scale(image, (80, 80))
                    draw_above.append((image, (i*64+15-8+tile.offset_x, j*64+15-8+tile.offset_y)))
                else:
                    self.screen.blit(image, (i*64+15, j*64+15))
        
        for stuff in draw_above:
            self.screen.blit(stuff[0], stuff[1])

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