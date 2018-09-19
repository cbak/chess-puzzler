import pygame

import board
import position        
    
def main():
    """ Main program function. """
    pygame.init()
    size = [board.BOARD_SIZE, board.BOARD_SIZE]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Chess Puzzle Trainer")

    done = False
    clock = pygame.time.Clock()

    start_board = board.ChessBoard()

    while not done:
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # game logic
        

        # draw chess board
        start_board.draw_board(screen, board.BOARD_SIZE, board.BLUE)
        start_board.populate_board(screen)

        # Pause for the next frame
        clock.tick(1)

    pygame.quit()

if __name__ == "__main__":
    main()
