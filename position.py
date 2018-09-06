import re
import sys

class ChessPosition:
    '''Represents a static chess position.'''

    __fen_regex__ = ('([\dBbKkNnPpQqRr]{1,8}/){7}[\dBbKkNnPpQqRr]{1,8} '
                     '[wb] ((K?Q?k?q?)|-) (([a-h][1-8])|-) \d{1,2} \d{1,4}')

    __fen_start__ = ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR '
                     'w KQkq - 0 1')
                
    def __fen_to_position__(self, fen): 
        '''Converts an FEN string into the chess position it represents.'''

        matchObj = re.match(self.__fen_regex__, fen)
        if not matchObj:
            raise ValueError('Invalid FEN string.')
            
        self.board = [['-'] * 8 for i in range(8)] # Create empty chess board
        rows = fen.split('/')
        data = rows[7].split(' ') 
        rows[7] = data[0]
        for cur_row, row in enumerate(rows):
            cur_col = 0
            for c in row:
                if c.isalpha():
                    self.board[cur_row][cur_col] = c
                    cur_col += 1
                elif c.isdigit():
                    cur_col += int(c)

        self.turn = data[1]
        self.castling = data[2]
        self.en_passant = data[3]

    def __init__(self, fen = __fen_start__):
        '''Initialises a 2-dimensional array from an FEN string. The default
            FEN describes the starting position of a chess game.'''
        self.__fen_to_position__(fen)

    def print_board(self):
        '''Prints the chess position'''
        for row in self.board:
            print(row)

    def print_info(self):
        '''Prints the FEN information'''
        print('%s to move.' % self.turn.upper())
        if self.castling == '-':
            print('Neither side can castle.')
        else:
            print('Castling: %s' % self.castling)
        if self.en_passant != '-':
            print('En passant available on %s.' % self.en_passant)

    def print_position(self):
        '''Prints the position and the FEN information'''
        print(' ')
        self.print_board()
        print(' ')
        self.print_info()
        print(' ')

start = ChessPosition()
start.print_position()
