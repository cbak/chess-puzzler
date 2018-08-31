import sys

class ChessBoard:
   """Represents a chess board."""

   def __fen_to_board__(self, fen): 
      """Converts an FEN string into the chess position it represents."""
      self.board = [["-"] * 8 for i in range(8)]
      rows = fen.split("/")
      # Truncate the final row to remove the remainder of the FEN string.
      rows[7] = rows[7].split(" ")[0]
      for cur_row, row in enumerate(rows):
         if len(row) > 8:
            sys.exit("Error: Too many characters in a row")
         cur_col = 0
         for c in row:
            if c.isalpha():
               self.board[cur_row][cur_col] = c
               cur_col += 1
            elif c.isdigit():
               cur_col += int(c)
            else: 
               print("Error: Invalid character %c." % (c))
               break
            if cur_col > 8:
               sys.exit("Error: Invalid row (%d): too many columns accounted for." % (cur_row))
         cur_row += 1
            
   def __init__(self, fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
      """Initialises a 2-dimensional array representing the
         starting position of a chess game."""
      self.__fen_to_board__(fen)


   def print_board(self):
      """Prints the chess board"""
      for row in self.board:
         print(row)

board1 = ChessBoard("5k2/8/8/8/4p3/3p4/1K6/7Q w - - 0 56")
board1.print_board()

