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
        
