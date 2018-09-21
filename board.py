"""
Module responsible for the graphical chess board.
"""

import os
import pygame

import position

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (125, 150, 255)
RED = (255, 100, 100)

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 600

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
    """ Graphical chess board. Subclass of Position.

    Attributes:
        piece_list: A group of PieceImage objects representing all
                    the pieces on the board.

    Methods: draw_board, update_board

    """
    def __init__(self, fen): 
        super().__init__(fen)
        self.piece_list = pygame.sprite.Group()

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

    def draw_board(self, screen, size, colour):
        """ Draw a chessboard.

        Args: screen: pygame surface.
              size (int): width/height of chessboard.
              colour (rgb tuple): colour of dark squares.

        """
        screen.fill(WHITE)

        def draw_squares(square_size, x_start, y_start):
            """ Draw squares on a series of rows in a chessboard pattern.

            Args: square_size (int): width/height of a square
                  x_start (int): x-coordinate of first square in a row.
                  y_start (int): y-coordinate of first square in a row.

            """
            for x in range(x_start, size, square_size*2):
                for y in range(y_start, size, square_size*2): 
                    dark_square = (x, y, square_size, square_size)
                    pygame.draw.rect(screen, colour, dark_square) 

        draw_squares(SQUARE_SIZE, 0, SQUARE_SIZE)
        draw_squares(SQUARE_SIZE, SQUARE_SIZE, 0)
        
        self.piece_list.draw(screen)

        # Draw the text box at the bottom of the screen
        pygame.draw.line(screen, BLACK, (0, BOARD_SIZE), 
                         (SCREEN_WIDTH, BOARD_SIZE), 5)

        text_rect = (0, BOARD_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT - BOARD_SIZE)
        pygame.draw.rect(screen, colour, text_rect) 


    def update_board(self, screen):
        pass
    
    def get_square(self, pos):
        """ Return the square contaning the passed position.

        Args: pos (int, int): position of the mouse cursor.

        """
        def get_coordinate(loc):
            if loc == 0:
                return 0
            else:
                return loc // SQUARE_SIZE
        
        x = get_coordinate(pos[1])
        y = get_coordinate(pos[0])

        return (x, y)

