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
            # get the legals for each cell
            cellLegals = getCellLegals(board, i, j)
            # check that cell has legals (not filled)
            if len(cellLegals) > 0:
                # assign a [] of legals to that cell
                legals[(i, j)] = [l for l in cellLegals]

    return legals


def fillUpdateBoardLegals(board, row, col):
    # update board legals when a cell is filled
    v = board.board[row][col]

    # update this cell's legals
    board.legals.pop((row, col))

    rowBlockStart = row // 3 * 3
    rowBlockEnd = rowBlockStart + 3
    colBlockStart = col // 3 * 3
    colBlockEnd = colBlockStart + 3

    # update region cells legals - same row, same col, or same block
    emptyLegals = set()
    for cell, legals in board.legals.items():
        if (row == cell[0] or col == cell[1] or
                (rowBlockStart <= cell[0] < rowBlockEnd and colBlockStart <= cell[1] < colBlockEnd)):
            if v in legals:
                legals.remove(v)
                if len(legals) == 0:
                    emptyLegals.add(cell)

    # remove any empty legals
    for cell in emptyLegals:
        board.legals.pop(cell)

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

# optimization function
def checkSolverDeadend(board, row, col, v):
    # check by putting v in (row, col) we end up
    # with empty cells that have no legals
    rowBlockStart = row // 3 * 3
    rowBlockEnd = rowBlockStart + 3
    colBlockStart = col // 3 * 3
    colBlockEnd = colBlockStart + 3

    # update region cells legals - same row, same col, or same block
    for cell, legals in board.legals.items():
        if row == cell[0] and col == cell[1]:
            # same cell, skip it
            continue

        if (row == cell[0] or col == cell[1] or
                (rowBlockStart <= cell[0] < rowBlockEnd and colBlockStart <= cell[1] < colBlockEnd)):
            if v in legals:
                if len(legals) == 1:
                    # a cell with single legal which is the same value - we have a deadend
                    return True

    return False

def getEmtpyCellCount(board):
    emptyCount = 0
    for row in board:
        for cell in row:
            if cell == 0:
                emptyCount += 1
    return emptyCount


class Board:
    def __init__(self, board):
        self.board = board
        self.rowCount = len(board)
        self.colCount = len(board[0])
        self.legals = getBoardLegals(board)
        self.emptyCount = getEmtpyCellCount(board)

    def fillCell(self, row, col, value):
        # can't fill this cell - has a value in it
        if self.board[row][col] != 0:
            return False

        cellLegals = self.legals[(row, col)]
        # check if the value is legal
        if value not in cellLegals:
            return False

        self.board[row][col] = value
        fillUpdateBoardLegals(self, row, col)
        #self.legals = getBoardLegals(self.board)
        self.emptyCount -= 1

        return True

    def isSolved(self):
        # for row in self.board:
        #     if 0 in row:
        #         return False
        # return True
        return self.emptyCount == 0

    # for testing
    def print(self):
        columns = '  '.join([str(i) for i in range(self.colCount)])
        print('   ' + columns)

        i = 0
        for row in self.board:
            print(i, row)
            i += 1

    # for removing values from a cell
    def emptyCell(self, row, cell):
        if self.board[row][cell] != 0:
            self.board[row][cell] = 0
            self.legals = getBoardLegals(self.board)
            self.emptyCount += 1

    # backtracker
    def solve(self):
        cell = getSolverCellCandidate(self)
        if cell == None:
            return self.isSolved()

        # try to solve using legals
        legals = self.legals[cell]
        for number in legals:
            # optimization
            if checkSolverDeadend(self, cell[0], cell[1], number):
                # not a good option, skip it
                continue

            self.fillCell(cell[0], cell[1], number)
            # if it can be solved return true
            if self.solve():
                return True
            # otherwise empty the cell
            self.emptyCell(cell[0], cell[1])

        # not resolved
        return False

    def getHint(self):
        # try to get an obvious single hint
        hint = getBoardObviousSingle(self)
        if hint != None:
            return hint

        # otherwise get an obvious tuple hint
        return getBoardObviousTuples(self)

    def applyHint(self, hint):
        # if there is no hint a hint cannot be applied
        if hint == None:
            return False

        # apply an obvious single hint
        if hint.region == 'cell':
            cell = hint.cells[0]
            hints = self.legals[cell]
            self.fillCell(cell[0], cell[1], hints[0])
            return True

        # otherwise apply an obvious tuple hint
        return appyBoardObviousTuples(self, hint)
    