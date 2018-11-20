"""
Defines a class ChessPosition that represents static chess position.
"""

import piece
import re

FEN_START = (
    'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
) 


class Position:
    """Represents a static chess position.

    Attributes:
        FEN (str): FEN representation of a chess position.
        board (str[][]): Textual representation of a chess position.
        turn (str): The player to move ('w' or 'b').
        castling (str): The castling rights of both players.
        en_passant (str): The square on which an en passant capture can
                          be made on the following move (if any).
        white_king (int, int): Location of the white king.
        black_king (int, int): Location of the black king.

    Methods: generate_fen, square, algebraic, update_position, print_board,
             print_info, print_position

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
        self.fen = fen
        white_king_count = 0
        black_king_count = 0
        self.board = [['-'] * 8 for i in range(8)]
        rows = fen.split('/')
        data = rows[7].split(' ')
        rows[7] = data[0]
        for cur_row, row in enumerate(rows):
            cur_col = 0
            for entry in row:
                if entry.isalpha():
                    if cur_col >= 8:
                        raise ValueError('Invalid FEN: too many columns.')
                    self.board[cur_row][cur_col] = entry
                    if entry == 'K':
                        if white_king_count > 0:
                            raise ValueError('Invalid FEN: too many kings.')
                        self.white_king = cur_row, cur_col
                        white_king_count += 1
                    if entry == 'k':
                        if black_king_count > 0:
                            raise ValueError('Invalid FEN: too many kings.')
                        self.black_king = cur_row, cur_col
                        black_king_count += 1
                    cur_col += 1
                elif entry.isdigit():
                    cur_col += int(entry)
        if white_king_count == 0 or black_king_count == 0:
            raise ValueError('Invalid FEN: not enough kings.')

        self.turn = data[1]
        self.castling = data[2]
        self.en_passant = data[3]

    def generate_fen(self):
        """ Generate FEN from the class attributes. """
        fen = []
        for cur_row, row in enumerate(self.board):
            blanks = 0
            for square in row:
                if square.isalpha():
                    if blanks > 0:
                        fen.append(str(blanks))
                        blanks = 0
                    fen.append(square)
                elif square == '-':
                    blanks += 1
                else:
                    raise ValueError('Board corrupted.')
            if blanks > 0:
                fen.append(str(blanks))
                blanks = 0
            if cur_row < 7:
                fen.append('/')
            elif cur_row == 7:
                fen.append(' ')

        fen.append(self.turn + ' ')
        fen.append(self.castling + ' ')
        fen.append(self.en_passant + ' 0 1')

        fen_string = ''.join(fen)
        return fen_string

    def square(self, algebraic):
        """ Translate square to array coordinates. 
        
        Arg: algebraic (string): Algebraic coordinates of a square. """
        row = 8 - int(algebraic[1])
        column = ord(algebraic[0]) - ord('a')
        return (row, column)

    def algebraic(self, square):
        """ Translate square to algebraic coordinates.

        Args: square (int, int): Array coordinates of a square. """
        rank = str(8 - square[0])
        file = chr(ord('a') + square[1])
        return file + rank

    def is_check(self):
        if self.turn == 'w':
            king_square = self.white_king
            filter = lambda p : p.symbol.isupper()
        if self.turn == 'b':
            king_square = self.black_king
            filter = lambda p : p.symbol.lower()

        for pieceobject in piece.Piece:
            if filter(pieceobject): 
                continue
            if king_square in piece.calculate_scope(self):
                return True

        return False

    def make_move(self, piece, end):
        """ Update the board. Return data to undo the update. """
        start = piece.square
        symbol = piece.symbol
        castle = None

        if self.board[end[0]][end[1]] == '-':
            capture = None
        else:
            capture = end, self.board[end[0]][end[1]]
        
        self.board[start[0]][start[1]] = '-'
        self.board[end[0]][end[1]] = symbol
        
        # Process en passant capture.
        if self.algebraic(end) == self.en_passant:
            if symbol == 'P':
                self.board[end[0]+1][end[1]] = '-'
                capture = (end[0]+1, end[1]), self.board[end[0]+1][end[1]]
            elif symbol == 'p':
                self.board[end[0]-1][end[1]] = '-'
                capture = (end[0]-1, end[1]), self.board[end[0]-1][end[1]]

        return start, symbol, end, capture, castle

    def undo_move(self, move_data):
        start, symbol, end, capture, castle = move_data
        self.board[start[0]][start[1]] = symbol
        self.board[end[0]][end[1]] = '-'

        if capture is not None:
            cap_sqr, cap_piece = capture
            self.board[cap_sqr[0]][cap_sqr[1]] = cap_piece

    def update_position(self, move_data):
        """ Update the position according to a move.
            Return data to be used in updating graphical board:
               piece_sprite: piece sprite to move
               end: destination square
               capture_square: square of captured piece. None if no capture.
               castle: (start, end) square of second moving piece.
                         None if the move made is not castling.

        Args: move_data: Tuple containing the piece sprite and end square.
        """
        piece_sprite, end = move_data 
        start, symbol, end, capture, castle = self.make_move(piece_sprite.piece, end)

        if self.turn == 'w':
            self.turn = 'b'
        elif self.turn == 'b':
            self.turn = 'w'

        # Update en passant square.
        if symbol == 'P' and start[0] == 6 and end[0] == 4:
            self.en_passant = self.algebraic((5, start[1]))
        elif symbol == 'p' and start[0] == 1 and end[0] == 3:
            self.en_passant = self.algebraic((2, start[1]))
        else:
            self.en_passant = '-'
        
        if capture is not None:
            capture_square, captured_piece = capture
        else:
            capture_square = None

        self.fen = self.generate_fen()

        return piece_sprite, end, capture_square, castle

    def print_board(self):
        """Print the chess position."""
        map(print, self.board)

    def print_info(self):
        """Print the FEN information."""
        print('%s to move.' % self.turn.upper())
        if self.castling == '-':
            print('Neither side can castle.')
        else:
            print('Castling: %s' % self.castling)
        if self.en_passant != '-':
            print('En passant available on %s.' % self.en_passant)
        print('White king is at %s.' % str(self.white_king))
        print('Black king is at %s.' % str(self.black_king))

    def print_position(self):
        """Print the chess position and the FEN information."""
        print(' ')
        self.print_board()
        print(' ')
        self.print_info()
        print(' ')

