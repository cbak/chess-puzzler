from abc import ABC, abstractmethod

class PieceFactory:
    @staticmethod
    def create(symbol, square):
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
    @abstractmethod
    def calculate_scope(self, position):
        pass

    def is_legal_move(self, position, dest_square):
        """ Return True if the move is legal, False otherwise. 

        Args: position (Position): Current position.
              start (int, int): Square currently occupied.
              dest_square (int, int): Proposed destination square.
        """
        if dest_square in self.calculate_scope(position):
            return True
        else:
            return False

    def update_square(self, square):
        self.square = square

    def algebraic_to_square(self, coordinates):
        row = 8 - int(coordinates[1])
        column = ord(coordinates[0]) - ord('a')
        return (row, column)

    def generate_diagonals(self):
        x = self.square[0]
        y = self.square[1]
        diagonals = [[]]
        
        diagonals.append( ( (x+a, y+a) for a in range(1,8) ) )
        diagonals.append( ( (x+a, y-a) for a in range(1,8) ) )
        diagonals.append( ( (x-a, y+a) for a in range(1,8) ) )
        diagonals.append( ( (x-a, y-a) for a in range(1,8) ) )
        
        return diagonals

    def generate_lines(self):
        x = self.square[0]
        y = self.square[1]
        lines = [[]]
        
        lines.append( ( (x, y+a) for a in range(1,8) ) )
        lines.append( ( (x+a, y) for a in range(1,8) ) )
        lines.append( ( (x, y-a) for a in range(1,8) ) )
        lines.append( ( (x-a, y) for a in range(1,8) ) )
        
        return lines

    def test_and_add_square(self, scope, board, row, col, test):
        if row < 0 or row > 7:
            return False
        if col < 0 or col > 7:
            return False
        if test(board[row][col]):
            scope.append((row, col))
            return True
        else:
            return False

    def test_and_add_squares_until(self, scope, board, squares, test, capture):
        """ 
        squares: square generator
        """
        for (row, col) in squares:
            result = self.test_and_add_square(scope, board, row, col, test)
            if result == False or capture(board[row][col]):
                break


class Pawn(Piece):
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
                square = self.algebraic_to_square(position.en_passant)
                if col != 0 and square == (up_one, col-1):
                    scope.append((up_one, col-1))
                if col != 7 and square == (up_one, col+1):
                    scope.append((up_one, col+1))
            
        if self.symbol.isupper():
            test_and_add_squares(row-1, row-2, 6, str.islower)
        else:   
            test_and_add_squares(row+1, row+2, 1, str.isupper)

        return scope
        
    def get_en_passant_square(self, dest_square):
        if self.symbol == 'P' and self.square[0] == 6 and dest_square[0] == 4:
            return (5, self.square[1])
        elif self.symbol == 'p' and self.square[0] == 1 and dest_square[0] == 3:
            return (2, self.square[1])
        else:
            return '-'
        

class Knight(Piece):
    def __init__(self, symbol, square):
        self.symbol = symbol 
        self.square = square

    def calculate_scope(self, position):
        scope = []
        board = position.board
        row = self.square[0]
        col = self.square[1]
        if self.symbol.isupper():
            test = lambda x : x == '-' or x.islower()
        if self.symbol.islower():
            test = lambda x : x == '-' or x.isupper()

        self.test_and_add_square(scope, board, row+1, col+2, test)
        self.test_and_add_square(scope, board, row+2, col+1, test)
        self.test_and_add_square(scope, board, row+2, col-1, test)
        self.test_and_add_square(scope, board, row+1, col-2, test)
        self.test_and_add_square(scope, board, row-1, col-2, test)
        self.test_and_add_square(scope, board, row-2, col-1, test)
        self.test_and_add_square(scope, board, row-2, col+1, test)
        self.test_and_add_square(scope, board, row-1, col+2, test)

        return scope


class Bishop(Piece):
    def __init__(self, symbol, square):
        self.symbol = symbol 
        self.square = square

    def calculate_scope(self, position):
        scope = []
        board = position.board
        row = self.square[0]
        col = self.square[1]
        if self.symbol.isupper():
            test = lambda x : x == '-' or x.islower()
            capture = lambda x : x.islower()
        if self.symbol.islower():
            test = lambda x : x == '-' or x.isupper()
            capture = lambda x : x.isupper()

        diagonals = self.generate_diagonals()

        for diagonal in diagonals:
            self.test_and_add_squares_until(
                scope, board, diagonal, test, capture
            )
        return scope


class Rook(Piece):
    def __init__(self, symbol, square):
        self.symbol = symbol 
        self.square = square

    def calculate_scope(self, position):
        scope = []
        board = position.board
        row = self.square[0]
        col = self.square[1]
        if self.symbol.isupper():
            test = lambda x : x == '-' or x.islower()
            capture = lambda x : x.islower()
        if self.symbol.islower():
            test = lambda x : x == '-' or x.isupper()
            capture = lambda x : x.isupper()

        lines = self.generate_lines()

        for line in lines:
            self.test_and_add_squares_until(
                scope, board, line, test, capture
            )
        return scope


class Queen(Piece):
    def __init__(self, symbol, square):
        self.symbol = symbol 
        self.square = square

    def calculate_scope(self, position):
        scope = []
        board = position.board
        row = self.square[0]
        col = self.square[1]
        if self.symbol.isupper():
            test = lambda x : x == '-' or x.islower()
            capture = lambda x : x.islower()
        if self.symbol.islower():
            test = lambda x : x == '-' or x.isupper()
            capture = lambda x : x.isupper()

        diagonals = self.generate_diagonals()
        for diagonal in diagonals:
            self.test_and_add_squares_until(
                scope, board, diagonal, test, capture
            )
        lines = self.generate_lines()
        for line in lines:
            self.test_and_add_squares_until(
                scope, board, line, test, capture
            )
        return scope


class King(Piece):
    def __init__(self, symbol, square):
        self.symbol = symbol 
        self.square = square
        
    def calculate_scope(self, position):
        scope = []
        board = position.board
        row = self.square[0]
        col = self.square[1]
        if self.symbol.isupper():
            test = lambda x : x == '-' or x.islower()
        if self.symbol.islower():
            test = lambda x : x == '-' or x.isupper()

        self.test_and_add_square(scope, board, row, col+1, test)
        self.test_and_add_square(scope, board, row+1, col+1, test)
        self.test_and_add_square(scope, board, row+1, col, test)
        self.test_and_add_square(scope, board, row+1, col-1, test)
        self.test_and_add_square(scope, board, row, col-1, test)
        self.test_and_add_square(scope, board, row-1, col-1, test)
        self.test_and_add_square(scope, board, row-1, col, test)
        self.test_and_add_square(scope, board, row-1, col+1, test)

        return scope
