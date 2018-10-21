"""
Defines a class ChessPosition that represents static chess position.
"""

import re
import sys

FEN_START = (
    'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
) 


class Position:
    """Represents a static chess position.

    Attributes:
        board (str[][]): Textual representation of a chess position.
        turn (str): The player to move ('w' or 'b').
        castling (str): The castling rights of both players.
        en_passant (str): The square on which an en passant capture can
                          be made on the following move (if any).

    Methods: print_board, print_info, print_position

    """ 
    FEN_REGEX = (
        '([\dBbKkNnPpQqRr]{1,8}/){7}[\dBbKkNnPpQqRr]{1,8} '
        '[wb] ((K?Q?k?q?)|-) (([a-h][1-8])|-) \d{1,2} \d{1,4}'
    )


    def __init__(self, fen):
        """Initialise the position from an FEN string.

        Args: fen (str): FEN string describing a chess position.

        """
        matchObj = re.match(Position.FEN_REGEX, fen)
        if not matchObj:
            raise ValueError('Invalid FEN.')
        self.board = [['-'] * 8 for i in range(8)]
        rows = fen.split('/')
        data = rows[7].split(' ') 
        rows[7] = data[0]
        for cur_row, row in enumerate(rows):
            cur_col = 0
            for c in row:
                if c.isalpha():
                    if cur_col >= 8:
                        raise ValueError('Invalid FEN: too many columns.')
                    self.board[cur_row][cur_col] = c
                    cur_col += 1
                elif c.isdigit():
                    cur_col += int(c)

        self.turn = data[1]
        self.castling = data[2]
        self.en_passant = data[3]
    
    def algebraic_to_square(self, coordinates):
        row = 8 - int(coordinates[1])
        column = ord(coordinates[0]) - ord('a')
        return (row, column)

    def square_to_algebraic(self, square):
        rank = str(8 - square[0])
        file = chr(ord('a') + square[1])
        return file + rank

    def update_position(self, symbol, start, end):
        """ Update the position according to a move.
            Return the updated squares.
        """
        updated = UpdatedSquares()

        self.board[start[0]][start[1]] = '-'
        self.board[end[0]][end[1]] = symbol
        updated.add_moved_piece(start, end)
        updated.set_clear_square(end)

        if self.turn == 'w':
            self.turn = 'b'
        elif self.turn == 'b':
            self.turn = 'w'

        # Process en passant capture.
        if self.square_to_algebraic(end) == self.en_passant:
            if symbol == 'P':
                self.board[end[0]+1][end[1]] = '-'
                updated.set_clear_square((end[0]+1, end[1]))
            elif symbol == 'p':
                self.board[end[0]-1][end[1]] = '-'
                updated.set_clear_square((end[0]-1, end[1]))
            else:
                raise ValueError('Piece moved to en passant square not a pawn.')
            
        # Update en passant square.
        if symbol == 'P' and start[0] == 6 and end[0] == 4:
            self.en_passant = self.square_to_algebraic((5, start[1]))
        elif symbol == 'p' and start[0] == 1 and end[0] == 3:
            self.en_passant = self.square_to_algebraic((2, start[1]))
        else:
            self.en_passant = '-'

        return updated
        
    def print_board(self):
        """Print the chess position."""
        for row in self.board:
            print(row)

    def print_info(self):
        """Print the FEN information."""
        print('%s to move.' % self.turn.upper())
        if self.castling == '-':
            print('Neither side can castle.')
        else:
            print('Castling: %s' % self.castling)
        if self.en_passant != '-':
            print('En passant available on %s.' % self.en_passant)

    def print_position(self):
        """Print the chess position and the FEN information."""
        print(' ')
        self.print_board()
        print(' ')
        self.print_info()
        print(' ')

class UpdatedSquares:
    """ Describes squares that are updated in a single move.

    Attributes: 
        moving_pieces ((int, int)[]): start and end squares of pieces to move.
        clear (int, int): square containing a captured piece.
            Only possible to capture one piece in a single move.
    """
    def __init__(self):
        self.moving_pieces = []
        self.clear = None

    def add_moved_piece(self, start, end):
        self.moving_pieces.append((start, end))

    def set_clear_square(self, square):
        self.clear = square
        
