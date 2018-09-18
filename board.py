"""
Module responsible for the graphical chess board.
"""

import os
import pygame

import position

WHITE = (255, 255, 255)
BLUE = (125, 150, 255)
RED = (255, 100, 100)

BOARD_WIDTH = 600
BOARD_HEIGHT = 600

SQUARE_WIDTH = 75
SQUARE_HEIGHT = 75

piece_sprites = {
    'P': 'white-pawn.png',
    'N': 'white-knight.png',
    'B': 'white-bishop.png',
    'R': 'white-rook.png',
    'Q': 'white-queen.png',
    'K': 'white-king.png',
    'p': 'black-pawn.png',
    'n': 'black-knight.png',
    'b': 'black-bishop.png',
    'r': 'black-rook.png',
    'q': 'black-queen.png',
    'k': 'black-king.png'
}

class PieceImage(pygame.sprite.Sprite):
    """ Represents a chess piece. """
    def __init__(self, piece, dir='img'):
        """ Load a chess piece sprite. 
        
        Args: piece (str): Character representation of a chess piece.
              dir (str): Directory containing the image files.
        
        """
        super().__init__()

        filename = piece_sprites[piece]
        file = os.path.join(dir, filename)
        self.image = pygame.image.load(file)

        # Convert to the correct pixel format
        self.image.convert() 
        
        # Set the transparent background colour
        self.image.set_colorkey(WHITE)

        # Fetch the rectangle object with dimensions of the loaded image.
        self.rect = self.image.get_rect()


class ChessBoard(position.Position):
    """ Graphical chess board. Subclass of Position 

    Attributes:
        piece_list: A group of PieceImage objects representing all
                    the pieces on the board.

    Methods: draw_board, populate_board, update_board

    """
    def __init__(self):
        super().__init__()
        self.piece_list = pygame.sprite.Group()

    def draw_board(self, screen, width, height, colour):
        """ Draw an empty chessboard.

        Args: screen: pygame surface.
              width (float): width of chessboard.
              height (float): height of chessboard.
              colour (rgb tuple): colour of dark squares.

        """
        screen.fill(WHITE)

        # Draw light squares on rows 1,3,5,7 from the top.
        for x in range(0, width, width//4):
            for y in range(height//8, height, height//4): 
                light_square = [x, y, width//8, height//8]
                pygame.draw.rect(screen, colour, light_square) 

        # Draw dark squares on rows 2,4,6,8 from the top.
        for x in range(width//8, width, width//4):
            for y in range(0, height, height//4): 
                dark_square = [x, y, width//8, height//8]
                pygame.draw.rect(screen, colour, dark_square) 

    def populate_board(self, screen):
        """ Draw the pieces according to the board attribute.

        Args: screen: pygame surface.

        """
        for row, rank in enumerate(self.board):
            # y-coordinate of row centre 
            y = SQUARE_HEIGHT * row      
            for column, piece in enumerate(rank):
                # x-coordinate of column centre
                x = SQUARE_WIDTH * column
                if piece.isalpha():
                    piece_sprite = PieceImage(piece)
                    piece_sprite.rect.x = x
                    piece_sprite.rect.y = y
                    self.piece_list.add(piece_sprite)

        self.piece_list.draw(screen)
        # Update the screen
        pygame.display.flip()

    # def update_board(move):
