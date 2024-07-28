class Board:
    def __init__(self, board):
        rowCount = len(board)
        colCount = len(board[0])

        self.board = board
        self.rowCount = rowCount
        self.colCount = colCount