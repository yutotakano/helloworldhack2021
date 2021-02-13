from game import Game

game = Game() 
game.randomize_board()
game.update_display()

# Game loop
while True:

    # Get all events currently in que, and handle them accordingly
    game.handle_events()
    # Refresh screen
    game.update_display()
