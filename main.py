import pygame

import graphics
import position        
    
def main():
    """ Main program function. """
    pygame.init()
    pygame.font.init()

    size = [graphics.SCREEN_WIDTH, graphics.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Chess Puzzle Trainer")

    running = True
    clock = pygame.time.Clock()
    board = graphics.Board(position.FEN_START)
    board.populate_piece_list()
    board.draw_board(screen, graphics.BOARD_SIZE)

    while running:
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                board.erase_text(screen)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for piece in board.piece_list:
                    if piece.rect.collidepoint(event.pos):
                        piece.selected = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if board.board_rect.collidepoint(event.pos):
                    updated_rects = board.update_board(screen, event.pos)

        # game logic

        # Update the screen
        if board.whole_board_update():
            pygame.display.update()
        else:
            pygame.display.update(board.updated_rects)
            board.clear_updated_rects()

        # Pause for the next frame
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
