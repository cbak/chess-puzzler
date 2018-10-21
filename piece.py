from abc import ABC, abstractmethod

class PieceFactory:
    """ Factory to create Piece subclasses. """
    @staticmethod
    def create(symbol, square):
        """ Creates an object depending on the 'symbol' parameter. 
        
        Args: symbol (str): character describing the piece.
              square (int, int): current location of the piece.
        """
        piece_class = None
        if symbol == 'P' or symbol == 'p':
            piece_class = Pawn
        elif symbol == 'N' or symbol == 'n':
            piece_class = Knight
        elif symbol == 'B' or symbol == 'b':
            piece_class = Bishop
        elif symbol == 'R' or symbol == 'r':
            piece_class = Rook
        elif symbol == 'Q' or symbol == 'q':
            piece_class = Queen
        elif symbol == 'K' or symbol == 'k':
            piece_class = King
        else:
            raise ValueError('Unexpected piece {}'.format(piece))

        return piece_class(symbol, square)


class Piece(ABC):
    """ Abstract class representing a chess piece.

    Attributes:
        symbol (str): character describing the piece.
        square (int, int): current location of the piece.

    Methods:
        calculate_scope, is_legal_move, generate_diagonals, generate_lines,
        test_and_add_squares, test_and_add_squares_until
    """
    @abstractmethod
    def calculate_scope(self, position):
        pass

    def is_legal_move(self, position, dest_square):
        """ Return True if the move is legal, False otherwise. 

        Args: position (Position): Current position.
              dest_square (int, int): Proposed destination square.
        """
        if dest_square in self.calculate_scope(position):
            return True
        else:
            return False

    def generate_diagonals(self):
        """ Return a list of generators of diagonals extending from the 
            piece's square. """
        x = self.square[0]
        y = self.square[1]
        diagonals = [[]]
        
        diagonals.append( ( (x+a, y+a) for a in range(1,8) ) )
        diagonals.append( ( (x+a, y-a) for a in range(1,8) ) )
        diagonals.append( ( (x-a, y+a) for a in range(1,8) ) )
        diagonals.append( ( (x-a, y-a) for a in range(1,8) ) )
        
        return diagonals

    def generate_lines(self):
        """ Return a list of generators of horizontal and vertical lines
            extending from the piece's square. """
        x = self.square[0]
        y = self.square[1]
        lines = [[]]
        
        lines.append( ( (x, y+a) for a in range(1,8) ) )
        lines.append( ( (x+a, y) for a in range(1,8) ) )
        lines.append( ( (x, y-a) for a in range(1,8) ) )
        lines.append( ( (x-a, y) for a in range(1,8) ) )
        
        return lines

    def test_and_add_square(self, scope, board, row, col, test):
        """ Add a square to the scope if it passes a test. 
            Return True if the square passes the test. False otherwise.
        
        Args: scope ((int, int)[]): List of squares in a piece's range.
              board (str[][]): Textual representation of a chess position.
              row (int): First index of square.
              col (int): Second index square.
              test (str -> bool): If True, add the square to the scope.
        """
        if row < 0 or row > 7:
            return False
        if col < 0 or col > 7:
            return False
            
        if test(board[row][col]):
            scope.append((row, col))
            return True
        else:
            return False

    def test_and_add_squares_until(self, scope, board, squares, test, fail):
        """ Test and add a sequence of squares to scope until failure.

        Args: scope ((int, int)[]): List of squares in a piece's range.
              board (str[][]): Textual representation of a chess position.
              squares: Generator of squares created by self.generate_diagonals
                       or self.generate_lines
              test (str -> bool): If True, add the square to the scope.
              fail (str -> bool): If False, don't test any more squares.  
        """
        for (row, col) in squares:
            result = self.test_and_add_square(scope, board, row, col, test)
            if result == False or fail(board[row][col]):
                break


class Pawn(Piece):
    """ Class representing a pawn. Subclass of Piece. 
    
    Attributes:
        symbol (str): character describing the piece.
        square (int, int): current location of the piece.

    Methods:
        calculate_scope, test_and_add_squares
    """
    def __init__(self, symbol, square):
        self.symbol = symbol
        self.square = square
    
    def calculate_scope(self, position):
        scope = []
        board = position.board
        row = self.square[0]
        col = self.square[1]

        # Unlike other chess pieces, pawns do not move and capture in 
        # the same way. Define a dedicated helper function to test 
        # the appropriate squares.
        def test_and_add_squares(up_one, up_two, second_row, test):
            # Check square in front of the pawn is empty.
            if board[up_one][col] == '-':
                scope.append((up_one, col))
                # If pawn is on second row, check two squares in front.
                if row == second_row and board[up_two][col] == '-':
                    scope.append((up_two, col))
            # Check front diagonal squares for enemy pieces.
            if col != 0 and test(board[up_one][col-1]):
                scope.append((up_one, col-1))     
            if col != 7 and test(board[up_one][col+1]):
                scope.append((up_one, col+1))
            # Check the en passant square. If it exists, test if it is empty.
            if position.en_passant != '-':
                square = position.algebraic_to_square(position.en_passant)
                if col != 0 and square == (up_one, col-1):
                    scope.append((up_one, col-1))
                if col != 7 and square == (up_one, col+1):
                    scope.append((up_one, col+1))
            
        if self.symbol.isupper():
            test_and_add_squares(row-1, row-2, 6, str.islower)
        else:   
            test_and_add_squares(row+1, row+2, 1, str.isupper)

        return scope
        

class Knight(Piece):
    """ Class representing a knight. Subclass of Piece. 
    
    Attributes:
        symbol (str): character describing the piece.
        square (int, int): current location of the piece.

    Methods:
        calculate_scope
    """
    def __init__(self, symbol, square):
        self.symbol = symbol 
        self.square = square

    def calculate_scope(self, position):
        scope = []
        board = position.board
        row = self.square[0]
        col = self.square[1]
        if self.symbol.isupper():
            is_free_square = lambda x : x == '-' or x.islower()
        if self.symbol.islower():
            is_free_square = lambda x : x == '-' or x.isupper()

        self.test_and_add_square(scope, board, row+1, col+2, is_free_square)
        self.test_and_add_square(scope, board, row+2, col+1, is_free_square)
        self.test_and_add_square(scope, board, row+2, col-1, is_free_square)
        self.test_and_add_square(scope, board, row+1, col-2, is_free_square)
        self.test_and_add_square(scope, board, row-1, col-2, is_free_square)
        self.test_and_add_square(scope, board, row-2, col-1, is_free_square)
        self.test_and_add_square(scope, board, row-2, col+1, is_free_square)
        self.test_and_add_square(scope, board, row-1, col+2, is_free_square)

        return scope


class Bishop(Piece):
    """ Class representing a bishop. Subclass of Piece. 
    
    Attributes:
        symbol (str): character describing the piece.
        square (int, int): current location of the piece.

    Methods:
        calculate_scope
    """
    def __init__(self, symbol, square):
        self.symbol = symbol 
        self.square = square

    def calculate_scope(self, position):
        scope = []
        board = position.board
        row = self.square[0]
        col = self.square[1]
        if self.symbol.isupper():
            is_free_square = lambda x : x == '-' or x.islower()
            capture = lambda x : x.islower()
        if self.symbol.islower():
            is_free_square = lambda x : x == '-' or x.isupper()
            capture = lambda x : x.isupper()

        diagonals = self.generate_diagonals()

        for diagonal in diagonals:
            self.test_and_add_squares_until(
                scope, board, diagonal, is_free_square, capture
            )
        return scope


class Rook(Piece):
    """ Class representing a rook. Subclass of Piece. 
    
    Attributes:
        symbol (str): character describing the piece.
        square (int, int): current location of the piece.

    Methods:
        calculate_scope
    """
    def __init__(self, symbol, square):
        self.symbol = symbol 
        self.square = square

    def calculate_scope(self, position):
        scope = []
        board = position.board
        row = self.square[0]
        col = self.square[1]
        if self.symbol.isupper():
            is_free_square = lambda x : x == '-' or x.islower()
            capture = lambda x : x.islower()
        if self.symbol.islower():
            is_free_square = lambda x : x == '-' or x.isupper()
            capture = lambda x : x.isupper()

        lines = self.generate_lines()

        for line in lines:
            self.test_and_add_squares_until(
                scope, board, line, is_free_square, capture
            )
        return scope


class Queen(Piece):
    """ Class representing a queen. Subclass of Piece. 
    
    Attributes:
        symbol (str): character describing the piece.
        square (int, int): current location of the piece.

    Methods:
        calculate_scope
    """
    def __init__(self, symbol, square):
        self.symbol = symbol 
        self.square = square

    def calculate_scope(self, position):
        scope = []
        board = position.board
        row = self.square[0]
        col = self.square[1]
        if self.symbol.isupper():
            is_free_square = lambda x : x == '-' or x.islower()
            capture = lambda x : x.islower()
        if self.symbol.islower():
            is_free_square = lambda x : x == '-' or x.isupper()
            capture = lambda x : x.isupper()

        diagonals = self.generate_diagonals()
        for diagonal in diagonals:
            self.test_and_add_squares_until(
                scope, board, diagonal, is_free_square, capture
            )
        lines = self.generate_lines()
        for line in lines:
            self.test_and_add_squares_until(
                scope, board, line, is_free_square, capture
            )
        return scope


class King(Piece):
    """ Class representing a king. Subclass of Piece. 
    
    Attributes:
        symbol (str): character describing the piece.
        square (int, int): current location of the piece.

    Methods:
        calculate_scope
    """
    def __init__(self, symbol, square):
        self.symbol = symbol 
        self.square = square
        
    def calculate_scope(self, position):
        scope = []
        board = position.board
        row = self.square[0]
        col = self.square[1]
        if self.symbol.isupper():
            is_free_square = lambda x : x == '-' or x.islower()
        if self.symbol.islower():
            is_free_square = lambda x : x == '-' or x.isupper()

        self.test_and_add_square(scope, board, row,   col+1, is_free_square)
        self.test_and_add_square(scope, board, row+1, col+1, is_free_square)
        self.test_and_add_square(scope, board, row+1, col,   is_free_square)
        self.test_and_add_square(scope, board, row+1, col-1, is_free_square)
        self.test_and_add_square(scope, board, row,   col-1, is_free_square)
        self.test_and_add_square(scope, board, row-1, col-1, is_free_square)
        self.test_and_add_square(scope, board, row-1, col,   is_free_square)
        self.test_and_add_square(scope, board, row-1, col+1, is_free_square)

        return scope
