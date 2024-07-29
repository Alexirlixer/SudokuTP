from boards.hints import *


def getCellLegals(board, row, col):
    if board[row][col] != 0:
        return {}

    # 1..9 are all legal initially
    legals = {i for i in range(1, 10)}

    # remove any number already in the row
    for i in range(len(board[row])):
        v = board[row][i]
        if v in legals:
            legals.remove(v)

    # remove any number already in the col
    for i in range(len(board)):
        v = board[i][col]
        if v in legals:
            legals.remove(v)

    rowStart = row // 3 * 3
    colStart = col // 3 * 3

    # remove any number already in the block
    for i in range(rowStart, rowStart + 3):
        for j in range(colStart, colStart + 3):
            v = board[i][j]
            if v in legals:
                legals.discard(v)

    return legals


def getBoardLegals(board):
    rowCount = len(board)
    colCount = len(board[0])

    legals = {}
    for i in range(rowCount):
        for j in range(colCount):
            cellLegals = getCellLegals(board, i, j)
            if len(cellLegals) > 0:
                legals[(i, j)] = [l for l in cellLegals]

    return legals


def getSolverCellCandidate(board):
    bestCell = None
    bestLen = 10

    # get next best cell to solve
    for cell, legals in board.legals.items():
        if len(legals) == 1:
            return cell
        if len(legals) < bestLen:
            bestLen = len(legals)
            bestCell = cell

    return bestCell


class Board:
    def __init__(self, board):
        self.board = board
        self.rowCount = len(board)
        self.colCount = len(board[0])
        self.legals = getBoardLegals(board)

    def fillCell(self, row, col, value):
        if self.board[row][col] != 0:
            return False

        cellLegals = self.legals[(row, col)]
        if value not in cellLegals:
            return False

        self.board[row][col] = value
        self.legals = getBoardLegals(self.board)

        return True

    def isSolved(self):
        if len(self.legals) == 0:
            return True

        return False

    def print(self):
        columns = '  '.join([str(i) for i in range(self.colCount)])
        print('   ' + columns)

        i = 0
        for row in self.board:
            print(i, row)
            i += 1

    def emptyCell(self, row, cell):
        self.board[row][cell] = 0
        self.legals = getBoardLegals(self.board)

    def solve(self):
        cell = getSolverCellCandidate(self)
        if cell == None:
            return self.isSolved()

        # try to solve using legals
        legals = self.legals[cell]
        for number in legals:
            self.fillCell(cell[0], cell[1], number)
            if self.solve():
                return True
            self.emptyCell(cell[0], cell[1])

        # not resolved
        return False

    def getHint(self):
        hint = getBoardObviousSingle(self)
        if hint != None:
            return hint

        return getBoardObviousTuples(self)

    def applyHint(self, hint):
        if hint == None:
            return False

        # single obvious
        if hint.region == 'cell':
            cell = hint.cells[0]
            hints = self.legals[cell]
            self.fillCell(cell[0], cell[1], hints[0])
            return True

        return appyBoardObviousTuples(self, hint)