import pygame

import board
import position        
    
def main():
    """ Main program function. """
    pygame.init()

    pygame.font.init()
    text_font = pygame.font.SysFont('Calibri', 36)

    size = [board.SCREEN_WIDTH, board.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Chess Puzzle Trainer")

    running = True
    clock = pygame.time.Clock()
    chessboard = board.ChessBoard(position.FEN_START)

    while running:
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pass

        # game logic
        chessboard.update_board(screen)

        # draw chess board
        chessboard.draw_board(screen, board.BOARD_SIZE, board.BLUE)

        # Update the screen
        pygame.display.flip()

        # Pause for the next frame
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
