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
LIGHT = WHITE
DARK = BLUE

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
    """ Represents a chess piece.
    
    Attributes: 
        image: PNG image loaded from a file.
        rect: Rect describing the location occupied by the image.
        selected: True if the piece has been clicked by the user.

    Methods: update

    """
    def __init__(self, piece, x, y, square, dir='img'):
        """ Load a chess piece sprite. 
        
        Args: piece (str): Character representation of a chess piece.
              x (int): x-coordinate of the sprite's Rect.
              y (int): y-coordinate of the sprite's Rect.
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
        self.image.set_colorkey(LIGHT)

        # Fetch the rectangle object with dimensions of the loaded image.
        self.rect = self.image.get_rect()

        # Initialise remaining attributes.
        self.piece = piece
        self.rect.x = x
        self.rect.y = y
        self.selected = False

    
    def update(self, location, promotion=None):
        """ Update the piece's location.
        
        Args: location (int, int): New coordinates.
              promotion (str): Promotion piece selected by user.
        """
        if location[0] < 0 or location[0] > BOARD_SIZE:
            return

        if location[1] < 0 or location[1] > BOARD_SIZE:
            return

        self.rect.x = location[0]
        self.rect.y = location[1]
        self.selected = False

        #TODO: Implement promotion (load new sprite to piece.image)
                        

class ChessBoard(position.Position):
    """ Graphical chess board. Subclass of Position.

    Attributes:
        piece_list: A group of PieceImage objects representing all
                    the pieces on the board.
        moving_pieces: A group of PieceImage objects to be moved.
        updated_rects: A list of Rects to be updated on the next frame.

    Methods: populate_piece_list, draw_board, get_square, get_corner,
             reset_square, update_board, whole_board_update, 
             clear_updated_rects, print_to_screen, erase_text
    """
    def __init__(self, fen): 
        super().__init__(fen)
        self.piece_list = pygame.sprite.Group()
        self.moving_pieces = pygame.sprite.Group()
        self.updated_rects = []

    def populate_piece_list(self):
        """ Initialise the PieceImage objects for every piece.
        
            The attributes (x, y) specify the coordinates of the top
            left corner of the square occupied by the piece. """
        for row, rank in enumerate(self.board):
            # y-coordinate of top border of the row 
            y = SQUARE_SIZE * row      
            for column, piece in enumerate(rank):
                # x-coordinate of left border of the column
                x = SQUARE_SIZE * column
                if piece.isalpha():
                    piece_sprite = PieceImage(piece, x, y, (row, column))
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

    def get_square(self, pos, square_size):
        """ Return row and column of square pointed at by cursor
        
        Args: pos (int, int): (x, y) position of the mouse cursor.
              square_size (int): Width and height of a square.
        """
        def get_coordinate(point):
            if point == 0:
                return 0
            elif point == BOARD_SIZE:
                return 7
            else:
                return point // square_size
        
        row = get_coordinate(pos[1])
        column = get_coordinate(pos[0])

        return (row, column)
    
    def reset_square(self, screen, square, square_size):
        """ Redraw the background of a square. Return the modified Rect.

        Args: screen: The active pygame surface.
              square (int, int): Row and column of a square.
              square_size (int): Width and height of a square.
        """
        if (square[0] + square[1]) % 2 == 0:
            colour = LIGHT
        else:
            colour = DARK
        
        # Get top left corner coordinates of the square.
        corner = (square[1] * square_size, square[0] * square_size)

        erased_rect = pygame.Rect(
            corner[0], corner[1], square_size, square_size
        )
        pygame.draw.rect(screen, colour, erased_rect)

        return erased_rect

    def update_board(self, screen, pos):
        """ Update the board according to user input. 

        Args: screen: Active pygame surface.
              pos (int, int): Coordinates of mouse cursor.

        """
        self.moving_pieces.empty()
        selected = None
        target = None

        for piece in self.piece_list:
            if piece.selected:
                selected = piece
            if piece.rect.collidepoint(pos) == True:
                target = piece

        if selected is None or selected is target:
            return

        current_pos = (selected.rect.x, selected.rect.y)
        src_square = self.get_square(current_pos, SQUARE_SIZE)
        dest_square = self.get_square(pos, SQUARE_SIZE)

        # if is_valid_move(args):

        # Redraw background of source and destination squares.
        src_rect = self.reset_square(screen, src_square, SQUARE_SIZE)
        dest_rect = self.reset_square(screen, dest_square, SQUARE_SIZE)
        self.updated_rects.append(src_rect)
        self.updated_rects.append(dest_rect)
        
        # Remove sprite occupying the target square.
        self.piece_list.remove(target)

        # Get top left corner coordinates of the destination square.
        location = (dest_square[1] * SQUARE_SIZE, dest_square[0] * SQUARE_SIZE)

        # Update location of moved pieces.
        selected.update(location)
        self.moving_pieces.add(selected)
        self.moving_pieces.draw(screen)


    def whole_board_update(self):
        """ Return True if the entire surface needs to be updated. """
        return self.updated_rects == []

    def clear_updated_rects(self):
        self.updated_rects = []

    def print_to_screen(self, screen, text, x_offset, y_offset):
        """ Print text to the screen below the chessboard.

        Args: screen: Active pygame surface.
              text (str): Text to print.
              x_offset (int): Distance of text from left side of screen.
              y_offset (int): Distance of text from the top of the text area.
        
        """
        text_font = pygame.font.SysFont('Arial', 16)
        screen_text = text_font.render(text, True, BLACK)
        screen.blit(screen_text, (x_offset, BOARD_SIZE + y_offset))

    def erase_text(self, screen, colour):
        """ Clears the text area. 

        Args: screen: Active pygame surface.
              colour (rgb tuple): Colour of background of text area.

        """
        text_rect = (0, BOARD_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT - BOARD_SIZE)
        pygame.draw.rect(screen, colour, text_rect) 
        

