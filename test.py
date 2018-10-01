"""
Module for unit testing.
"""

import sys
import unittest

import position

class TestChessPosition(unittest.TestCase):
    FEN_POSITIONS = [ 
        ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR '
         'w KQkq - 0 1',
         [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
          ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
          ['-', '-', '-', '-', '-', '-', '-', '-'],
          ['-', '-', '-', '-', '-', '-', '-', '-'],
          ['-', '-', '-', '-', '-', '-', '-', '-'],
          ['-', '-', '-', '-', '-', '-', '-', '-'],
          ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
          ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]
        ),

        ('8/8/1q6/2k5/4K3/5Q2/8/8 w - - 0 1',
         [['-', '-', '-', '-', '-', '-', '-', '-'],
          ['-', '-', '-', '-', '-', '-', '-', '-'],
          ['-', 'q', '-', '-', '-', '-', '-', '-'],
          ['-', '-', 'k', '-', '-', '-', '-', '-'],
          ['-', '-', '-', '-', 'K', '-', '-', '-'],
          ['-', '-', '-', '-', '-', 'Q', '-', '-'],
          ['-', '-', '-', '-', '-', '-', '-', '-'],
          ['-', '-', '-', '-', '-', '-', '-', '-']]
        ),

        ('r2qk2r/pp3ppp/2nb1n2/2p1p3/2PpP1b1/3P1NP1/PP2NPBP/'
         'R1BQ1RK1 b kq c3 0 9',
         [['r', '-', '-', 'q', 'k', '-', '-', 'r'],
          ['p', 'p', '-', '-', '-', 'p', 'p', 'p'],
          ['-', '-', 'n', 'b', '-', 'n', '-', '-'],
          ['-', '-', 'p', '-', 'p', '-', '-', '-'],
          ['-', '-', 'P', 'p', 'P', '-', 'b', '-'],
          ['-', '-', '-', 'P', '-', 'N', 'P', '-'],
          ['P', 'P', '-', '-', 'N', 'P', 'B', 'P'],
          ['R', '-', 'B', 'Q', '-', 'R', 'K', '-']]
        )
    ]

    FEN_INFO = [
        ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR '
         'w KQkq - 0 1',
         'W to move.\nCastling: KQkq\n'),

        ('8/8/1q6/2k5/4k3/5Q2/8/8 w - - 0 1',
         'W to move.\nNeither side can castle.\n'),

        ('r2qk2r/pp3ppp/2nb1n2/2p1p3/2PpP1b1/3P1NP1/PP2NPBP/'
         'R1BQ1RK1 b kq c3 0 9',
         'B to move.\nCastling: kq\nEn passant available on c3.\n')
    ]

    BAD_FENS = [
        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/ w KQkq - 0 1', 
        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR KQkq - 0 1',
        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - 0 1',
        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq 0 1',
        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 1',
        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkr - 0 1',
        'rnbqkbnr/ppppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
        '8/8/8/8/2p5p/8/8/8 w - - 0 1',
        '8K/8Q/8R/8R/8N/8B/8P w - - 0 1'
    ]

    def test_fen_to_board(self):
        """Test the board generation from FEN input.

        Initialising a position with an FEN string should generate 
        correct board with known input.
        
        """
        for fen, board in self.FEN_POSITIONS:
            test_position = position.Position(fen)
            self.assertEqual(test_position.board, board)

    def test_bad_fens(self):
        """Test incorrect FEN strings."""
        for fen in self.BAD_FENS:
            with self.assertRaises(ValueError): 
                test_position = position.Position(fen)

    def test_fen_infos(self):
        """Test the info generation from FEN input.

        Defines a helper class to temporarily replace sys.stdout in 
        order to capture the output of test_position with the 
        expected output.
        
        """
        class MyOutput:
            def __init__(self):
                self.data=[]

            def write(self, s):
                self.data.append(s)

            def clear(self):
                self.data=[]

            def __str__(self):
                return "".join(self.data)

        stdout_org = sys.stdout  # Preserve current state of stdout.
        my_stdout = MyOutput()

        for fen, info in self.FEN_INFO:
            try:
                sys.stdout = my_stdout
                test_position = position.Position(fen)
                test_position.print_info()
                self.assertEqual( str(my_stdout), info)
                my_stdout.clear()
            finally:
                sys.stdout = stdout_org  # Restore stdout state.


if __name__ == '__main__':
    main() 
