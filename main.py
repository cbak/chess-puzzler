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
    board.add_sprites()
    board.draw(screen, graphics.BOARD_SIZE)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                board.erase_text(screen)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                board.select_piece(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                move_data = board.process_move(screen, event.pos)
                if move_data is not None:
                    board_update_data = board.update_position(move_data)
                    board.update_board(screen, board_update_data)

        # Update the screen
        if board.whole_board_update():
            pygame.display.update()
        else:
            pygame.display.update(board.updated_rects)
            board.clear_updated_rects()

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
