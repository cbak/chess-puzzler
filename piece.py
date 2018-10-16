#import position

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

class Piece:

    def calculate_scope(self, position):
        pass
        # Abstract method

    def is_legal_move(self, position, end):
        """ Return True if the move is legal, False otherwise. 

        Args: position (Position): Current position.
              start (int, int): Square currently occupied.
              end (int, int): Proposed destination square.
        """
        pass
        # Abstract method

    def algebraic_to_square(self, coordinates):
        row = 8 - int(coordinates[1])
        column = ord(coordinates[0]) - ord('a')
        return (row, column)

class Pawn(Piece)
    def __init__(self, symbol, square):
        self.symbol = symbol
        self.square = square
        self.scope = []
    
    def calculate_scope(self, position):
        pass
        

    def is_legal_move(self, position, end):
        return True


class Knight(Piece)
    def __init__(self, symbol, square):
        self.symbol = symbol 
        self.square = square
        self.scope = []

    def calculate_scope(self, position):
        pass

    def is_legal_move(self, position, end):
        return True


class Bishop(Piece)
    def __init__(self, symbol, square):
        self.symbol = symbol 
        self.square = square
        self.scope = []

    def calculate_scope(self, position):
        pass

    def is_legal_move(self, position, end):
        return True


class Rook(Piece)
    def __init__(self, symbol, square):
        self.symbol = symbol 
        self.square = square
        self.scope = []

    def calculate_scope(self, position):
        pass

    def is_legal_move(self, position, end):
        return True

class Queen(Piece)
    def __init__(self, symbol, square):
        self.symbol = symbol 
        self.square = square
        self.scope = []

    def calculate_scope(self, position):
        pass

    def is_legal_move(self, position, end):
        return True

class King(Piece)
    def __init__(self, symbol, square):
        self.symbol = symbol 
        self.square = square
        self.scope = []
        
    def calculate_scope(self, position):
        pass

    def is_legal_move(self, position, end):
        return True

