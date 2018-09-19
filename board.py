"""
Module responsible for the graphical chess board.
"""

import os
import pygame

import position

WHITE = (255, 255, 255)
BLUE = (125, 150, 255)
RED = (255, 100, 100)

BOARD_SIZE = 600 
SQUARE_SIZE = BOARD_SIZE//8

piece_sprites = {
    'P': 'WhitePawn.png',
    'N': 'WhiteKnight.png',
    'B': 'WhiteBishop.png',
    'R': 'WhiteRook.png',
    'Q': 'WhiteQueen.png',
    'K': 'WhiteKing.png',
    'p': 'BlackPawn.png',
    'n': 'BlackKnight.png',
    'b': 'BlackBishop.png',
    'r': 'BlackRook.png',
    'q': 'BlackQueen.png',
    'k': 'BlackKing.png'
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
        picture = pygame.image.load(file)
        self.image = pygame.transform.scale(picture, 
                                           (SQUARE_SIZE, SQUARE_SIZE))

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

    def draw_board(self, screen, size, colour):
        """ Draw an empty chessboard.

        Args: screen: pygame surface.
              size (int): width/height of chessboard.
              colour (rgb tuple): colour of dark squares.

        """
        screen.fill(WHITE)

        # Draw dark squares on rows 1,3,5,7 from the top.
        for x in range(0, size, size//4):
            for y in range(SQUARE_SIZE, size, size//4): 
                dark_square = (x, y, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(screen, colour, dark_square) 

        # Draw dark squares on rows 2,4,6,8 from the top.
        for x in range(SQUARE_SIZE, size, size//4):
            for y in range(0, size, size//4): 
                dark_square = (x, y, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(screen, colour, dark_square) 

    def populate_board(self, screen):
        """ Draw the pieces according to the board attribute.

        Args: screen: pygame surface.

        """
        for row, rank in enumerate(self.board):
            # y-coordinate of row centre 
            y = SQUARE_SIZE * row      
            for column, piece in enumerate(rank):
                # x-coordinate of column centre
                x = SQUARE_SIZE * column
                if piece.isalpha():
                    piece_sprite = PieceImage(piece)
                    piece_sprite.rect.x = x
                    piece_sprite.rect.y = y
                    self.piece_list.add(piece_sprite)

        self.piece_list.draw(screen)
        # Update the screen
        pygame.display.flip()

    # def update_board(move):
