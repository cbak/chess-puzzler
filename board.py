import sys

class ChessPosition:
   """Represents a static chess position."""

   def __fen_to_position__(self, fen): 
      """Converts an FEN string into the chess position it represents."""
      self.position = [["-"] * 8 for i in range(8)]
      rows = fen.split("/")
      # The last string contains the piece data for the last row followed
      # by the metadata. 
      data = rows[7].split(" ") 
      rows[7] = data[0]
      for cur_row, row in enumerate(rows):
         if len(row) > 8:
            sys.exit("Error: Too many characters in a row")
         cur_col = 0
         for c in row:
            if c.isalpha():
               self.position[cur_row][cur_col] = c
               cur_col += 1
            elif c.isdigit():
               cur_col += int(c)
            else: 
               print("Error: Invalid character %c." % (c))
               break
            if cur_col > 8:
               sys.exit("Error: Too many columns in row %d." % (cur_row))
         cur_row += 1
      self.turn = data[1]
      self.castling = data[2]
      self.en_passant = data[3]
      self.fifty_move = data[4]
      self.move_number = data[5]

   __fen_start__ = ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR "
                    "w KQkq - 0 1")
            
   def __init__(self, fen = __fen_start__):
      """Initialises a 2-dimensional array from an FEN string. The default
         FEN describes the starting position of a chess game."""
      self.__fen_to_position__(fen)

   def print_position(self):
      """Prints the chess position"""
      print(" ")
      for row in self.position:
         print(row)
      print(" ")
      print("%s to move." % self.turn.upper())
      if self.castling == "-":
         print("Neither side can castle.")
      else:
         print("Castling: %s" % self.castling)
      if self.en_passant != "-":
         print("En passant available on %s" % self.en_passant)

position1 = ChessPosition()
position1.print_position()

