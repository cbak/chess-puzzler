"""
Module responsible for the graphical chess board.
"""

import os
import pygame

import piece
import position

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (125, 150, 255)
RED = (255, 100, 100)

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 600
    
BOARD_SIZE = 600
SQUARE_SIZE = BOARD_SIZE//8


class PieceSprite(pygame.sprite.Sprite):
    """ Represents a chess piece.
    
    Attributes: 
        image: PNG image loaded from a file.
        rect: Rect describing the location occupied by the image.
        piece: Piece object defined in module 'piece'.
        selected: True if the piece has been clicked and is being dragged
                  by the user. False otherwise.

    Methods: load_image, update

    """
    selected_count = 0

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

    def __init__(self, symbol, x, y, square, size, dir='img'):
        """ Constructor for PieceSprite. 
        
        Args: symbol (str): Character representing a piece.
              x (int): x-coordinate of the sprite's Rect.
              y (int): y-coordinate of the sprite's Rect.
              square (int, int): Current square of the piece.
              size (int): Width/height of square.
              dir (str): Directory containing the image files.
        
        """
        super().__init__()

        self.load_image(symbol, size, dir)

        # Fetch the rectangle object with dimensions of the loaded image.
        self.rect = self.image.get_rect()

        # Initialise remaining attributes.
        self.piece = piece.PieceFactory.create(symbol, square)
        self.rect.x = x
        self.rect.y = y
        self.selected = False

    def load_image(self, symbol, size, dir='img'):
        """ Load a chess piece sprite. 
        
        Args: symbol (str): Character representing a piece.
              size (int): Width/height of square.
              dir (str): Directory containing the image files.
        """

        filename = PieceSprite.piece_sprites[symbol]
        file = os.path.join(dir, filename)
        picture = pygame.image.load(file)
        self.image = pygame.transform.scale(picture, (size, size))
        # Convert to the correct pixel format
        self.image.convert() 
        # Set the transparent background colour
        self.image.set_colorkey(WHITE)

    
    def update(self, location, square, promotion=None):
        """ Update the piece's location.
        
        Args: location (int, int): New coordinates.
              square (int, int): New square.
              promotion (str): Promotion piece selected by user.
        """
        if location[0] < 0 or location[0] > BOARD_SIZE:
            return

        if location[1] < 0 or location[1] > BOARD_SIZE:
            return

        if promotion is not None:
            self.load_image(symbol, SQUARE_SIZE)

        self.rect.x = location[0]
        self.rect.y = location[1]
        self.piece.square = square


class Board(position.Position):
    """ Graphical chess board. Subclass of Position.

    Attributes:
        light: (rgb tuple): Colour of the light squares.
        dark: (rgb tuple): Colour of the dark squares.
        board_rect (pygame.Rect): Rect describing the chessboard region.
        piece_list: Group of PieceSprite objects representing all
                    the pieces on the board.
        moving_pieces: Group of PieceSprite objects to be moved.
        updated_rects: List of Rects to be updated on the next frame.
        text_box (graphics.TextBox): Text box object.
        
    Methods: add_sprites, draw, square_from_cursor, coordinates_from_square,
             clear_square, update, whole_board_update, clear_updated_rects,
    """

    def __init__(self, fen): 
        super().__init__(fen)
        self.light = WHITE
        self.dark = BLUE
        self.board_rect = pygame.Rect(0, 0, BOARD_SIZE, BOARD_SIZE)
        self.piece_list = pygame.sprite.Group()
        self.moving_pieces = pygame.sprite.Group()
        self.updated_rects = []
        text_rect = pygame.Rect(
            0, BOARD_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT - BOARD_SIZE
        )
        self.textbox = TextBox(text_rect, self.dark)

    def add_sprites(self):
        """ Initialise the PieceSprite objects for every piece on the board.
        
            The attributes (x, y) specify the coordinates of the top
            left corner of the square occupied by the piece. """
        for row, rank in enumerate(self.board):
            # y-coordinate of top border of the row 
            y = SQUARE_SIZE * row      
            for column, symbol in enumerate(rank):
                # x-coordinate of left border of the column
                x = SQUARE_SIZE * column
                if symbol.isalpha():
                    piece_sprite = PieceSprite(
                        symbol, x, y, (row, column), SQUARE_SIZE
                    )
                    self.piece_list.add(piece_sprite)

    def draw(self, screen, size):
        """ Draw a chessboard.

        Args: screen: pygame surface.
              size (int): width/height of chessboard.

        """
        screen.fill(self.light)

        def draw_squares(square_size, x_start, y_start):
            """ Draw squares on a series of rows in a chessboard pattern.

            Args: square_size (int): width/height of a square
                  x_start (int): x-coordinate of first square in a row.
                  y_start (int): y-coordinate of first square in a row.

            """
            for x in range(x_start, size, square_size*2):
                for y in range(y_start, size, square_size*2): 
                    dark_square = (x, y, square_size, square_size)
                    pygame.draw.rect(screen, self.dark, dark_square) 

        draw_squares(SQUARE_SIZE, 0, SQUARE_SIZE)
        draw_squares(SQUARE_SIZE, SQUARE_SIZE, 0)
        
        self.piece_list.draw(screen)

        self.textbox.draw(screen)

    def square_from_cursor(self, pos):
        """ Return row and column of square pointed at by cursor.
        
        Args: pos (int, int): (x, y) position of the mouse cursor.
        """
        def get_coordinate(point):
            if point == BOARD_SIZE:
                return 7
            else:
                return point // SQUARE_SIZE
        
        row = get_coordinate(pos[1])
        column = get_coordinate(pos[0])

        return (row, column)

    def coordinates_from_square(self, square):
        """ Return top left corner coordinates of a square. 
        
        Args: square (int, int): Array indices of a square. 
        """
        x = square[1] * SQUARE_SIZE
        y = square[0] * SQUARE_SIZE
        return x, y
    
    def clear_square(self, screen, square):
        """ Redraw the background of a square. Return the modified Rect.

        Args: screen: The active pygame surface.
              square (int, int): Row and column of a square.
        """
        if (square[0] + square[1]) % 2 == 0:
            colour = self.light
        else:
            colour = self.dark
        
        # Get top left corner coordinates of the square.
        corner = self.coordinates_from_square(square)
        
        erased_rect = pygame.Rect(
            corner[0], corner[1], SQUARE_SIZE, SQUARE_SIZE
        )
        pygame.draw.rect(screen, colour, erased_rect)

        return erased_rect

    def select_piece(self, pos):
        """ Mark a piece as selected if its sprite collides with 'pos'.

        Args: pos (int, int): Coordinates of mouse cursor.
        
        """
        if PieceSprite.selected_count > 0:
            raise ValueError("select_piece called when a piece is selected.")
        for piece_sprite in self.piece_list:
            if piece_sprite.rect.collidepoint(pos):
                piece_sprite.selected = True
                PieceSprite.selected_count += 1

    def process_move(self, screen, pos):
        """ Test a move indicated by user mouse movement.
            Return move data (piece symbol, start square, end square). 

        Args: screen: Active pygame surface.
              pos (int, int): Coordinates of mouse cursor.

        """
        if not self.board_rect.collidepoint(pos):
            return None

        selected_sprite = None
        for piece_sprite in self.piece_list:
            if piece_sprite.selected:
                selected_sprite = piece_sprite
        if selected_sprite is None: 
            return None

        dest_square = self.square_from_cursor(pos)
        selected = selected_sprite.piece

        if selected.legal_move(self, dest_square):
            return selected.symbol, selected.square, dest_square
        else:
            selected_sprite.selected = False
            PieceSprite.selected_count -= 1
            return None

    def find_piece_on_square(self, square):
        """ Search for a piece sprite whose square matches the passed square. 

            Args: square (int, int): Coordinates of a square.

        """
        for piece_sprite in self.piece_list:
            if piece_sprite.piece.square == square:
                return piece_sprite
        return

    def update_board(self, screen, updated_squares):
        """ Update the graphical board. 

        Args: screen: Active pygame surface.
              updated_squares: tuple describing the squares to update.
        """
        self.moving_pieces.empty()

        moving_pieces, clear_square = updated_squares
    
        # Delete captured piece sprite.
        captured_piece = self.find_piece_on_square(clear_square)
        self.piece_list.remove(captured_piece)
        dest_rect = self.clear_square(screen, clear_square)
        self.updated_rects.append(dest_rect)

        # Update squares and sprites for moving pieces.
        for move in moving_pieces:
            moving_piece = self.find_piece_on_square(move[0])
            src_rect = self.clear_square(screen, move[0])
            self.updated_rects.append(src_rect)
            location = self.coordinates_from_square(move[1])
            moving_piece.update(location, move[1])
            moving_piece.selected = False
            PieceSprite.selected_count -= 1
            self.moving_pieces.add(moving_piece)
            self.moving_pieces.draw(screen)

    def whole_board_update(self):
        """ Return True if the entire surface needs to be updated. """
        return self.updated_rects == []

    def clear_updated_rects(self):
        """ Empty the updated_rects field. """
        self.updated_rects = []

        
class TextBox:
    """ Describes and manages the text box below the chess board.

    Attributes:
        text_rect (pygame.Rect): Rect describing the text box region.
        border ((int, int), (int, int):
            Start and end coordinates of the border line.
        colour (rgb tuple): Background colour.
        font (pygame.Font): Text font.
        self.x_offset: Horizontal distance of next blank line,
                       from left of text_rect.
        self.y_offset: Vertical distance of next blank line,
                       from top of text_rect.
        
    Methods: draw, print, clear
    
    """
    def __init__(self, rect, colour):
        self.rect = rect
        self.border = ( (rect.left, rect.top+2),
                        (rect.left + rect.width, rect.top+2) )
        self.colour = colour
        self.font = pygame.font.SysFont('Arial', 16)
        self.x_offset = 20
        self.y_offset = BOARD_SIZE + 20

    def draw(self, screen):
        """ Draw the text box.

        Args: screen: Active pygame surface.
        
        """
        pygame.draw.rect(screen, self.colour, self.rect) 
        pygame.draw.line(screen, BLACK, self.border[0], self.border[1], 5)

    def print(self, screen, text):
        """ Print text in the text box.

        Args: screen: Active pygame surface.
              text (str): Text to print.        
        """
        screen_text = self.font.render(text, True, BLACK)
        screen.blit(screen_text, (self.x_offset, self.y_offset))
        self.y_offset += 20

    def clear(self, screen):
        """ Clear the text box. 

        Args: screen: Active pygame surface.

        """
        pygame.draw.rect(screen, self.colour, self.rect) 
        pygame.draw.line(screen, BLACK, self.border[0], self.border[1], 10)
        self.x_offset = 20
        self.y_offset = BOARD_SIZE + 20
