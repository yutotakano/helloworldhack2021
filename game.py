class Game:

    def __init__(self, pygame):
        self.board = [[None for i in range(5)] for i in range(5)]
        self.pygame = pygame
        self.points = 0
    
    def randomize_board(self):
        # TODO, update self.board in here
        pass

    def update_display(self):
        # screen.draw and stuff
        # TODO

        self.pygame.display.update()
    
    def remove_tile_at_pos(self, positions):
        # TODO: remove the tile at each position in the list
        # then move down anything above
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
        # TODO: switch the tiles at oldpos and newpos
        pass
        
    def on_drag_and_drop(self, oldpos, newpos):
        # called when a tile is dragged and dropped

        self.swap_tiles(oldpos, newpos)
        
        did_enter_loop = False
        
        # As long as a match exists, handle it
        while tile_positions := match_exists:
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

        if remaining_shuffle_count < 0:
            self.game_over()
        else:
            self.randomize_board()

    def game_over(self):
        # TODO:
        self.pygame.quit()
        pass