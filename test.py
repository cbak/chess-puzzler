import position
import unittest
import sys

class TestChessPosition(unittest.TestCase):

    fen_positions = ( ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR '
                       'w KQkq - 0 1',
                       [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]),

                      ('8/8/1q6/2k5/4K3/5Q2/8/8 w - - 0 1',
                       [['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', 'q', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', 'k', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', 'K', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', 'Q', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-']]),

                      ('r2qk2r/pp3ppp/2nb1n2/2p1p3/2PpP1b1/3P1NP1/PP2NPBP/'
                       'R1BQ1RK1 b kq c3 0 9',
                       [['r', '-', '-', 'q', 'k', '-', '-', 'r'],
                        ['p', 'p', '-', '-', '-', 'p', 'p', 'p'],
                        ['-', '-', 'n', 'b', '-', 'n', '-', '-'],
                        ['-', '-', 'p', '-', 'p', '-', '-', '-'],
                        ['-', '-', 'P', 'p', 'P', '-', 'b', '-'],
                        ['-', '-', '-', 'P', '-', 'N', 'P', '-'],
                        ['P', 'P', '-', '-', 'N', 'P', 'B', 'P'],
                        ['R', '-', 'B', 'Q', '-', 'R', 'K', '-']]))

    fen_info = (('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR '
                 'w KQkq - 0 1',
                 'W to move.\nCastling: KQkq\n'),

                ('8/8/1q6/2k5/4k3/5Q2/8/8 w - - 0 1',
                 'W to move.\nNeither side can castle.\n'),

                ('r2qk2r/pp3ppp/2nb1n2/2p1p3/2PpP1b1/3P1NP1/PP2NPBP/'
                 'R1BQ1RK1 b kq c3 0 9',
                 'B to move.\nCastling: kq\nEn passant available on c3.\n'))
                    
    def test_fen_to_board(self):
        '''Initialising a Position with an FEN string should generate correct
           board with known input.'''
        for fen, board in self.fen_positions:
            test_position = position.ChessPosition(fen)
            self.assertEqual(test_position.board, board)

    def test_fen_infos(self):
        ''' Defines a helper class to temporarily replace sys.stdout in 
            order to capture the output of test_position with the expected
            output.'''
        class MyOutput:
            def __init__(self):
                self.data=[]

            def write(self, s):
                self.data.append(s)

            def clear(self):
                self.data=[]

            def __str__(self):
                return "".join(self.data)

        ''' Preserve current state of stdout to restore after test.'''
        stdout_org = sys.stdout
        my_stdout = MyOutput()

        for fen, info in self.fen_info:
            try:
                sys.stdout = my_stdout
                test_position = position.ChessPosition(fen)
                test_position.print_info()
                self.assertEqual( str(my_stdout), info)
                my_stdout.clear()
            finally:
                sys.stdout = stdout_org


if __name__ == '__main__':
    unittest.main()

                 