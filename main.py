import pygame

import board
import position        
    
def main():
    """ Main program function. """
    pygame.init()
    pygame.font.init()

    size = [board.SCREEN_WIDTH, board.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Chess Puzzle Trainer")

    running = True
    clock = pygame.time.Clock()
    chessboard = board.ChessBoard(position.FEN_START)
    chessboard.populate_piece_list()
    chessboard.draw_board(screen, board.BOARD_SIZE, board.DARK)

    while running:
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                chessboard.erase_text(screen, board.DARK)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for piece in chessboard.piece_list:
                    if piece.rect.collidepoint(event.pos) == True:
                        piece.selected = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                updated_rects = chessboard.update_board(screen, event.pos)

        # game logic

        # Update the screen
        if chessboard.whole_board_update():
            pygame.display.update()
        else:
            pygame.display.update(chessboard.updated_rects)
            chessboard.clear_updated_rects()

        # Pause for the next frame
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
