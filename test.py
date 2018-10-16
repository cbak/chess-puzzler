"""
Module for unit testing.
"""

import sys
import unittest

import piece
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

class TestPiece(unittest.TestCase):

    def test_pawn_calculate_scope(self):
        
        pawn_fen = (
            'rn1qkb1r/2p1pppp/6B1/pp1pP3/P3b1n1/NP3P1P/2PP2P1/R1BQK1NR '
            'w KQkq d6 0 10'
        )
        pawn_pos = position.Position(pawn_fen)

        pawn_a4 = piece.PieceFactory.create('P', (4, 0))
        pawn_b3 = piece.PieceFactory.create('P', (5, 1))
        pawn_c2 = piece.PieceFactory.create('P', (6, 2))
        pawn_e5 = piece.PieceFactory.create('P', (3, 4))
        pawn_f3 = piece.PieceFactory.create('P', (5, 5))
        pawn_g2 = piece.PieceFactory.create('P', (6, 6))
        pawn_h3 = piece.PieceFactory.create('P', (5, 7))
        pawn_a5 = piece.PieceFactory.create('p', (3, 0))
        pawn_c7 = piece.PieceFactory.create('p', (1, 2))
        pawn_d5 = piece.PieceFactory.create('p', (3, 3))
        pawn_f7 = piece.PieceFactory.create('p', (1, 5))

        self.assertEqual(pawn_a4.calculate_scope(pawn_pos), [(3,1)])
        self.assertEqual(pawn_b3.calculate_scope(pawn_pos), [(4,1)])
        self.assertEqual(pawn_c2.calculate_scope(pawn_pos), [(5,2), (4,2)])
        self.assertEqual(pawn_e5.calculate_scope(pawn_pos), [(2,4), (2,3)])
        self.assertEqual(pawn_f3.calculate_scope(pawn_pos), 
                         [(4,5), (4,4), (4,6)])
        self.assertEqual(pawn_g2.calculate_scope(pawn_pos), [(5,6)])
        self.assertEqual(pawn_h3.calculate_scope(pawn_pos), [(4,7), (4,6)])
        self.assertEqual(pawn_a5.calculate_scope(pawn_pos), [])
        self.assertEqual(pawn_c7.calculate_scope(pawn_pos), [(2,2), (3,2)])
        self.assertEqual(pawn_d5.calculate_scope(pawn_pos), [(4,3)])
        self.assertEqual(pawn_f7.calculate_scope(pawn_pos),
                         [(2,5), (3,5), (2,6)])

    def test_bishop_calculate_scope(self):
                         
        bishop_fen = 'b7/4kbq1/b7/1n6/2RB4/1n5B/1K4P1/8 w - - 0 1'
        bishop_pos = position.Position(bishop_fen)

        bishop_a8 = piece.PieceFactory.create('b', (0, 0))
        bishop_a6 = piece.PieceFactory.create('b', (2, 0))
        bishop_a4 = piece.PieceFactory.create('b', (4, 0))
        bishop_d4 = piece.PieceFactory.create('B', (4, 3))
        bishop_h3 = piece.PieceFactory.create('B', (5, 7))

        self.assertEqual(bishop_a8.calculate_scope(pawn_pos),
                         [(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7)])
        self.assertEqual(bishop_a6.calculate_scope(bishop_pos),
                         [(1,1), (0,2)])
        self.assertEqual(bishop_a4.calculate_scope(bishop_pos), [])
        self.assertEqual(bishop_d4.calculate_scope(bishop_pos), 
                         [(3,2), (2,1), (1,0), (3,4), (2,5), (1,6), (5,4),
                          (6,5), (7,6), (5,2)])
        self.assertEqual(bishop_h3.calculate_scope(bishop_pos), 
                         [(4,6), (3,5), (2,4), (1,3), (0,2)])

    def test_knight_calculate_scope(self):
        
        knight_fen = 'N3k3/6n1/8/8/4n3/1PN3P1/P1PPPP1P/4K2N w - - 0 1'
        knight_pos = position.position(knight_fen)

        knight_a8 = piece.PieceFactory.create('N', (0,0))
        knight_g7 = piece.PieceFactory.create('n', (1,6))
        knight_e4 = piece.PieceFactory.create('n', (4,4))
        knight_c3 = piece.PieceFactory.create('N', (5,2))
        knight_h1 = piece.PieceFactory.create('N', (7,7))

        self.assertEqual(knight_a8.calculate_scope(knight_pos), 
                         [(1,2), (2,1)])
        self.assertEqual(knight_g7.calculate_scope(knight_pos), 
                         [(3,7), (3,5), (2,4)])
        self.assertEqual(knight_e4.calculate_scope(knight_pos), 
                         [(5,6), (6,5), (6,3), (5,2), (3,2), (2,3), (2,5),
                          (3,6)])
        self.assertEqual(knight_c3.calculate_scope(knight_pos), 
                         [(7,3), (7,1), (4,0), (3,1), (3,3), (4,4)])
        self.assertEqual(knight_h1.calculate_scope(knight_pos), [])

    def test_rook_calculate_scope(self):
        
        rook_fen = '4k3/ppp2pbp/6p1/8/3r4/2B3R1/P5PP/RN1QK3 w - - 0 1'
        rook_pos = position.position(rook_fen)

        rook_d4 = piece.PieceFactory.create('r', (4,3))
        rook_g3 = piece.PieceFactory.create('R', (5,6))
        rook_a1 = piece.PieceFactory.create('R', (7,0))

        self.assertEqual(rook_d4.calculate_scope(rook_pos), [(4,4), (4,5),
                         (4,6), (4,7), (5,3), (6,3), (7,3), (4,2), (4,1), 
                         (4,0), (3,3), (2,3), (1,3), (0,3)]) 
        self.assertEqual(rook_g3.calculate_scope(rook_pos), [(5,7), (5,5),
                         (5,4), (5,3), (4,6), (3,6), (2,6)])
        self.assertEqual(rook_a1.calculate_scope(rook_pos), [])

    def test_queen_calculate_scope(self):
        
        queen_fen = ('r1bqkbqr/pp2pppp/3p4/2p3Q1/2PnP3/8/PP3PPP/RNBQKBNR'
                     'w KQkq - 0 1')
        queen_pos = position.position(queen_fen)

        queen_d8 = piece.PieceFactory.create('q', (0,3))
        queen_g8 = piece.PieceFactory.create('q', (0,6))
        queen_g5 = piece.PieceFactory.create('Q', (3,6))
        queen_d1 = piece.PieceFactory.create('Q', (7,3))

        self.assertEqual(queen_d8.calculate_scope(queen_pos), [(1,3), (1,2),
                         (2,1), (3,0)]
        self.assertEqual(queen_g8.calculate_scope(queen_pos), [])
        self.assertEqual(queen_g5.calculate_scope(queen_pos), [(3,7), (4,7),
                         (4,6), (5,6), (4,5), (5,4), (6,3), (3,5), (3,4),
                         (3,3), (3,2), (2,5), (1,4), (2,6), (1,6)]
        self.assertEqual(queen_d1.calculate_scope(queen_pos), [(6,2), (5,1),
                         (4,0), (6,3), (5,3), (4,3), (6,4), (5,5), (4,6), 
                         (3,7)]
            
    def test_king_calculate_scope(self):
        
        king_fen = ('8/8/2k5/2n5/4q3/5KQ1/4B1R1/8 w - - 0 1')
        king_pos = position.position(king_fen)

        king_c6 = piece.PieceFactory.create('k', (2,2))
        king_f4 = piece.PieceFactory.create('K', (5,5))

        self.assertEqual(king_c6.calculate_scope(king_pos), [(2,3), (3,3),
                         (3,2), (3,1), (2,1), (1,1), (1,2), (1,3)]
        self.assertEqual(king_c6.calculate_scope(king_pos), [(6,5), (5,4),
                         (4,4), (4,5), (4,6)]

if __name__ == '__main__':
    main() 
