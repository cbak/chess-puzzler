"""
Module for unit testing.
"""

import pygame
import sys
import unittest

import graphics
import piece
import position

class TestPosition(unittest.TestCase):
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
         'R1BQ1RK1 b kq c3 0 1',
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
         'W to move.\nCastling: KQkq\n'
         'White king is at (7, 4).\nBlack king is at (0, 4).\n'),

        ('8/8/1q6/2k5/4K3/5Q2/8/8 w - - 0 1',
         'W to move.\nNeither side can castle.\n'
         'White king is at (4, 4).\nBlack king is at (3, 2).\n'),

        ('r2qk2r/pp3ppp/2nb1n2/2p1p3/2PpP1b1/3P1NP1/PP2NPBP/'
         'R1BQ1RK1 b kq c3 0 9',
         'B to move.\nCastling: kq\nEn passant available on c3.\n'
         'White king is at (7, 6).\nBlack king is at (0, 4).\n')
    ]

    BAD_FENS = [
        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/ w KQkq - 0 1', 
        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR KQkq - 0 1',
        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - 0 1',
        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq 0 1',
        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 1',
        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkr - 0 1',
        'rnbqkbnr/ppppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
        'rnbqqbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQQBNR w KQkq - 0 1',
        'rnbkkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBKKBNR w KQkq - 0 1',
        '8/8/8/8/2k5K/8/8/8 w - - 0 1',
        '8K/8Q/8R/8R/8N/8B/8P w - - 0 1'
    ]

    def test_generate_fen(self):
        for fen, board in self.FEN_POSITIONS:
            test_position = position.Position(fen)
            new_fen = test_position.generate_fen()
            self.assertEqual(new_fen, fen)

    def test_make_move(self):
        # Test a few moves in a fairly normal chess position.
        fen =  ('2rq1rk1/1b2bpp1/p2p1n1p/n1p1p1B1/Pp2P3/1NPP1N1P/1PB2PP1/'
                'R2QR1K1 w - a3 0 1')
        fen1 = ('2rq1rk1/1b2bpp1/p2p1n1p/n1p1p1B1/Pp2P1P1/1NPP1N1P/1PB2P2/'
                'R2QR1K1 w - a3 0 1')
        fen2 = ('2rq1rk1/1b2bpp1/p2p1B1p/n1p1p3/Pp2P1P1/1NPP1N1P/1PB2P2/'
                'R2QR1K1 w - a3 0 1')
        fen3 = ('2rq1rk1/1b2bpp1/p2p1B1p/n1p1p3/4P1P1/pNPP1N1P/1PB2P2/'
                'R2QR1K1 w - a3 0 1')
        fen4 = ('2rq1rk1/1b2bpp1/p2p1B1p/2p1p3/4P1P1/pnPP1N1P/1PB2P2/'
                'R2QR1K1 w - a3 0 1')
        fen5 = ('2r2rk1/1b2bpp1/pq1p1B1p/2p1p3/4P1P1/pnPP1N1P/1PB2P2/'
                'R2QR1K1 w - a3 0 1')

        moves_position = position.Position(fen)
        pawn_g2 = piece.PieceFactory.create('P', (6, 6))
        bishop_g5 = piece.PieceFactory.create('B', (3, 6))        
        pawn_b4 = piece.PieceFactory.create('p', (4, 1))
        knight_a5 = piece.PieceFactory.create('n', (3, 0))
        queen_d8 = piece.PieceFactory.create('q', (0, 3))

        moves_position.make_move(pawn_g2, (4, 6))
        new_fen = moves_position.generate_fen()
        self.assertEqual(new_fen, fen1)

        moves_position.make_move(bishop_g5, (2, 5))
        new_fen = moves_position.generate_fen()
        self.assertEqual(new_fen, fen2)

        moves_position.make_move(pawn_b4, (5, 0))
        new_fen = moves_position.generate_fen()
        self.assertEqual(new_fen, fen3)

        moves_position.make_move(knight_a5, (5, 1))
        new_fen = moves_position.generate_fen()
        self.assertEqual(new_fen, fen4)

        moves_position.make_move(queen_d8, (2, 1))
        new_fen = moves_position.generate_fen()
        self.assertEqual(new_fen, fen5)

        # Test all four castling moves.
        castling_fen = 'r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1' 
        castling_position = position.Position(castling_fen)
        king_e1 = piece.PieceFactory.create('K', (7, 4))
        king_e8 = piece.PieceFactory.create('k', (0, 4))

        wk_fen = 'r3k2r/8/8/8/8/8/8/R4RK1 w KQkq - 0 1'
        castling_position.make_move(king_e1, (7, 6))
        new_fen = castling_position.generate_fen()
        self.assertEqual(new_fen, wk_fen)

        castling_position = position.Position(castling_fen)
        wq_fen = 'r3k2r/8/8/8/8/8/8/2KR3R w KQkq - 0 1'
        castling_position.make_move(king_e1, (7, 2))
        new_fen = castling_position.generate_fen()
        self.assertEqual(new_fen, wq_fen)

        castling_position = position.Position(castling_fen)
        bk_fen = 'r4rk1/8/8/8/8/8/8/R3K2R w KQkq - 0 1'
        castling_position.make_move(king_e8, (0, 6))
        new_fen = castling_position.generate_fen()
        self.assertEqual(new_fen, bk_fen)

        castling_position = position.Position(castling_fen)
        bq_fen = '2kr3r/8/8/8/8/8/8/R3K2R w KQkq - 0 1'
        castling_position.make_move(king_e8, (0, 2))
        new_fen = castling_position.generate_fen()
        self.assertEqual(new_fen, bq_fen)

    def test_undo_move(self):
        fen =  ('2rq1rk1/1b2bpp1/p2p1n1p/n1p1p1B1/Pp2P3/1NPP1N1P/1PB2PP1/'
                'R2QR1K1 w - a3 0 1')

        moves_position = position.Position(fen)
        pawn_g2 = piece.PieceFactory.create('P', (6, 6))
        bishop_g5 = piece.PieceFactory.create('B', (3, 6))        
        pawn_b4 = piece.PieceFactory.create('p', (4, 1))
        knight_a5 = piece.PieceFactory.create('n', (3, 0))
        queen_d8 = piece.PieceFactory.create('q', (0, 3))

        move_data = moves_position.make_move(pawn_g2, (4, 6))
        moves_position.undo_move(move_data)
        new_fen = moves_position.generate_fen()
        self.assertEqual(new_fen, fen)

        move_data = moves_position.make_move(bishop_g5, (2, 5))
        moves_position.undo_move(move_data)
        new_fen = moves_position.generate_fen()
        self.assertEqual(new_fen, fen)

        move_data = moves_position.make_move(pawn_b4, (5, 0))
        moves_position.undo_move(move_data)
        new_fen = moves_position.generate_fen()
        self.assertEqual(new_fen, fen)

        move_data = moves_position.make_move(knight_a5, (5, 1))
        moves_position.undo_move(move_data)
        new_fen = moves_position.generate_fen()
        self.assertEqual(new_fen, fen)

        move_data = moves_position.make_move(queen_d8, (2, 1))
        moves_position.undo_move(move_data)
        new_fen = moves_position.generate_fen()
        self.assertEqual(new_fen, fen)

        # TODO: Add promotion test

    def test_is_check(self):
        # Create Board and call add_sprites to get a sprite list to pass to is_check.
        # Rest should be straightforward
        pass
    
    def test_is_legal_move(self):
        pass

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
            'rn1qkb1r/4pppp/2p3B1/pp1pP3/P3b1n1/NP3P1P/2PP2P1/R1BQK1NR '
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
        pawn_c6 = piece.PieceFactory.create('p', (2, 2))
        pawn_d5 = piece.PieceFactory.create('p', (3, 3))
        pawn_f7 = piece.PieceFactory.create('p', (1, 5))

        self.assertCountEqual(pawn_a4.calculate_scope(pawn_pos), [(3,1)])
        self.assertCountEqual(pawn_b3.calculate_scope(pawn_pos), [(4,1)])
        self.assertCountEqual(pawn_c2.calculate_scope(pawn_pos), 
            [(5,2), (4,2)]
        )
        self.assertCountEqual(pawn_e5.calculate_scope(pawn_pos), 
            [(2,4), (2,3)]
        )
        self.assertCountEqual(pawn_f3.calculate_scope(pawn_pos), 
            [(4,5), (4,4), (4,6)]
        )
        self.assertCountEqual(pawn_g2.calculate_scope(pawn_pos), [(5,6)])
        self.assertCountEqual(pawn_h3.calculate_scope(pawn_pos), 
            [(4,7), (4,6)]
        )
        self.assertCountEqual(pawn_a5.calculate_scope(pawn_pos), [])
        self.assertCountEqual(pawn_c6.calculate_scope(pawn_pos), [(3,2)])
        self.assertCountEqual(pawn_d5.calculate_scope(pawn_pos), [(4,3)])
        self.assertCountEqual(pawn_f7.calculate_scope(pawn_pos),
            [(2,5), (3,5), (2,6)]
        )

    def test_bishop_calculate_scope(self):
                         
        bishop_fen = 'b7/4kbq1/b7/1n6/2RB4/1n5B/1K4P1/8 w - - 0 1'
        bishop_pos = position.Position(bishop_fen)

        bishop_a8 = piece.PieceFactory.create('b', (0, 0))
        bishop_a6 = piece.PieceFactory.create('b', (2, 0))
        bishop_a4 = piece.PieceFactory.create('b', (4, 0))
        bishop_d4 = piece.PieceFactory.create('B', (4, 3))
        bishop_h3 = piece.PieceFactory.create('B', (5, 7))

        self.assertCountEqual(bishop_a8.calculate_scope(bishop_pos),
            [(1,1), (2,2), (3,3), (4,4), (5,5), (6,6)]
        )
        self.assertCountEqual(bishop_a6.calculate_scope(bishop_pos),
            [(1,1), (0,2)]
        )
        self.assertCountEqual(bishop_a4.calculate_scope(bishop_pos), [])
        self.assertCountEqual(bishop_d4.calculate_scope(bishop_pos), 
            [(3,2), (2,1), (1,0), (3,4), (2,5), (1,6), (5,4), (6,5), (7,6),
             (5,2)]
        )
        self.assertCountEqual(bishop_h3.calculate_scope(bishop_pos), 
            [(4,6), (3,5), (2,4), (1,3), (0,2)]
        )

    def test_knight_calculate_scope(self):
        
        knight_fen = 'N3k3/6n1/8/8/4n3/1PN3P1/P1PPPP1P/4K2N w - - 0 1'
        knight_pos = position.Position(knight_fen)

        knight_a8 = piece.PieceFactory.create('N', (0,0))
        knight_g7 = piece.PieceFactory.create('n', (1,6))
        knight_e4 = piece.PieceFactory.create('n', (4,4))
        knight_c3 = piece.PieceFactory.create('N', (5,2))
        knight_h1 = piece.PieceFactory.create('N', (7,7))

        self.assertCountEqual(knight_a8.calculate_scope(knight_pos), 
            [(1,2), (2,1)]
        )
        self.assertCountEqual(knight_g7.calculate_scope(knight_pos), 
            [(3,7), (3,5), (2,4)]
        )
        self.assertCountEqual(knight_e4.calculate_scope(knight_pos), 
            [(5,6), (6,5), (6,3), (5,2), (3,2), (2,3), (2,5), (3,6)]
        )
        self.assertCountEqual(knight_c3.calculate_scope(knight_pos), 
            [(7,3), (7,1), (4,0), (3,1), (3,3), (4,4)]
        )
        self.assertCountEqual(knight_h1.calculate_scope(knight_pos), [])

    def test_rook_calculate_scope(self):
        
        rook_fen = '4k3/ppp2pbp/6p1/8/3r4/2B3R1/P5PP/RN1QK3 w - - 0 1'
        rook_pos = position.Position(rook_fen)

        rook_d4 = piece.PieceFactory.create('r', (4,3))
        rook_g3 = piece.PieceFactory.create('R', (5,6))
        rook_a1 = piece.PieceFactory.create('R', (7,0))

        self.assertCountEqual(rook_d4.calculate_scope(rook_pos), 
           [(4,4), (4,5), (4,6), (4,7), (5,3), (6,3), (7,3), (4,2),
            (4,1), (4,0), (3,3), (2,3), (1,3), (0,3)]
        ) 
        self.assertCountEqual(rook_g3.calculate_scope(rook_pos), 
           [(5,7), (5,5), (5,4), (5,3), (4,6), (3,6), (2,6)]
        )
        self.assertCountEqual(rook_a1.calculate_scope(rook_pos), [])

    def test_queen_calculate_scope(self):
        
        queen_fen = ('r1bqkbqr/pp2pppp/3p4/2p3Q1/2PnP3/8/PP3PPP/RNBQKBNR '
                     'w KQkq - 0 1')
        queen_pos = position.Position(queen_fen)

        queen_d8 = piece.PieceFactory.create('q', (0,3))
        queen_g8 = piece.PieceFactory.create('q', (0,6))
        queen_g5 = piece.PieceFactory.create('Q', (3,6))
        queen_d1 = piece.PieceFactory.create('Q', (7,3))

        self.assertCountEqual(queen_d8.calculate_scope(queen_pos),
            [(1,3), (1,2), (2,1), (3,0)]
        )
        self.assertCountEqual(queen_g8.calculate_scope(queen_pos), [])
        self.assertCountEqual(queen_g5.calculate_scope(queen_pos), 
            [(3,7), (4,7), (4,6), (5,6), (4,5), (5,4), (6,3), (3,5), (3,4),
             (3,3), (3,2), (2,5), (1,4), (2,6), (1,6), (2,7)]
        )
        self.assertCountEqual(queen_d1.calculate_scope(queen_pos),
            [(6,2), (5,1), (4,0), (6,3), (5,3), (4,3), (6,4), (5,5), (4,6), 
             (3,7)]
        )

    def test_king_calculate_scope(self):
        
        king_fen = ('8/8/2k5/8/4q3/5KQ1/4B1R1/8 w - - 0 1')
        king_pos = position.Position(king_fen)

        king_c6 = piece.PieceFactory.create('k', (2,2))
        king_f4 = piece.PieceFactory.create('K', (5,5))

        self.assertCountEqual(king_c6.calculate_scope(king_pos),
            [(2,3), (3,3), (3,2), (3,1), (2,1), (1,1), (1,2), (1,3)]
        )
        self.assertCountEqual(king_f4.calculate_scope(king_pos),
            [(6,5), (5,4), (4,4), (4,5), (4,6)]
        )

        castling_fen = 'r3kb1r/8/8/8/8/8/8/1R2K2R w KQkq - 0 1' 
        castling_pos = position.Position(castling_fen)
        king_e1 = piece.PieceFactory.create('K', (7,4))
        king_e8 = piece.PieceFactory.create('k', (0,4))

        self.assertCountEqual(king_e1.calculate_scope(castling_pos),
            [(7,5), (7,6), (6,5), (6,4), (6,3), (7,3)])
        self.assertCountEqual(king_e8.calculate_scope(castling_pos),
            [(1,5), (1,4), (1,3), (0,3), (0,2)])

if __name__ == '__main__':
    main() 
