import math

from boards.hints import *
import statistics


def getCellLegals(board, row, col):
    # get all values that are legal for this cell
    # - values which are not already used in the row,
    # col or block the cell belongs to
    if board[row][col] != 0:
        return {}

    # assume all numbers from 1 to 9 are all legal initially
    # then gradually remove that is in use
    legals = {i for i in range(1, 10)}

    # remove any number already in the col
    for i in range(len(board[row])):
        v = board[row][i]
        if v in legals:
            legals.remove(v)

    # remove any number already in the row
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
    legals = {}
    rowCount = len(board)
    colCount = len(board[0])

    # collect legals for every cell in the board
    # and put them in a cell-based dictionary
    for i in range(rowCount):
        for j in range(colCount):
            cellLegals = getCellLegals(board, i, j)
            if len(cellLegals) > 0:
                legals[(i, j)] = [l for l in cellLegals]

    return legals


def fillUpdateBoardLegals(board, row, col):
    # update board legals when a cell is filled
    # this is an optimization so we do not recalculate legals for the entire board
    # instead, update only legals for the row, col and block the cell
    # belongs to
    v = board.board[row][col]

    # update this cell's legals
    board.legals.pop((row, col))

    # calculate block ranged
    rowBlockStart = row // 3 * 3
    rowBlockEnd = rowBlockStart + 3
    colBlockStart = col // 3 * 3
    colBlockEnd = colBlockStart + 3

    # update region cells legals - same row, same col, or same block
    emptyLegals = set()
    for cell, legals in board.legals.items():
        if (row == cell[0] or col == cell[1] or
                (rowBlockStart <= cell[0] < rowBlockEnd and colBlockStart <= cell[1] < colBlockEnd)):
            # check if the newly added value is in the cell's legals
            # and remove it if it is
            if v in legals:
                legals.remove(v)
                if len(legals) == 0:
                    emptyLegals.add(cell)

    # remove any empty legals
    for cell in emptyLegals:
        board.legals.pop(cell)


def getSolverCellCandidate(board):
    # get the empty cell with the minimum number
    # of legals
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


def checkSolverDeadend(board, row, col, v):
    # check if by putting v in (row, col) we end up
    # with empty cells that have no legals

    # calculate block ranges
    rowBlockStart = row // 3 * 3
    rowBlockEnd = rowBlockStart + 3
    colBlockStart = col // 3 * 3
    colBlockEnd = colBlockStart + 3

    # verify region cells legals - same row, same col, or same block
    for cell, legals in board.legals.items():
        if row == cell[0] and col == cell[1]:
            # same cell, skip it
            continue

        if (row == cell[0] or col == cell[1] or
                (rowBlockStart <= cell[0] < rowBlockEnd and colBlockStart <= cell[1] < colBlockEnd)):
            # check if the candidate value is in this cell's legals
            if v in legals:
                # if it is and we have only one legal it means if we remove it
                # we would end up with an empty cell with no legals - therefore
                # using this candidate value would lead to a dead end
                if len(legals) == 1:
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
        # attempt to put a value into a cell
        # will return true if success, false
        # if this was an incorrect value
        if self.board[row][col] != 0:
            return False
        # if (row, col) not in self.legals:
        #     return False

        cellLegals = self.legals[(row, col)]
        if value not in cellLegals:
            return False

        # the cell was empty and value was part of legals
        # - set the value and update board and legals
        self.board[row][col] = value
        fillUpdateBoardLegals(self, row, col)
        #self.legals = getBoardLegals(self.board)
        self.emptyCount -= 1

        return True

    def isSolved(self):
        return self.emptyCount == 0

    def print(self):
        # for debugging purposes
        columns = '  '.join([str(i) for i in range(self.colCount)])
        print('   ' + columns)

        i = 0
        for row in self.board:
            print(i, row)
            i += 1

    def emptyCell(self, row, cell):
        # attempt to remove value from a cell
        if self.board[row][cell] != 0:
            # this cell was not empty, empty it
            # and recalculate legas for the board
            self.board[row][cell] = 0
            self.legals = getBoardLegals(self.board)
            self.emptyCount += 1

    def solve(self):
        # backtracking solver which uses number of
        # legals to look for the best candidate
        cell = getSolverCellCandidate(self)
        if cell == None:
            return self.isSolved()

        # best candidate cell identified, try to solve sudoku using
        # its legals
        legals = self.legals[cell]
        for number in legals:
            # check if using this legal value would lead to a dead end
            # and skip it if yes
            if checkSolverDeadend(self, cell[0], cell[1], number):
                continue

            # good candidate, set it and attempt to sovlve the rest
            self.fillCell(cell[0], cell[1], number)
            if self.solve():
                return True

            # no solution, backtrack
            self.emptyCell(cell[0], cell[1])

        # not resolved
        return False

    def getHint(self):
        # get board hint. returns a "Hint" object which has
        # the region (from where it was extracted) and one or
        # more cells
        hint = getBoardObviousSingle(self)
        if hint != None:
            return hint

        return getBoardObviousTuples(self)

    def applyHint(self, hint):
        if hint == None:
            return False

        # single obvious - apply it directly
        if hint.region == 'cell':
            cell = hint.cells[0]
            hints = self.legals[cell]
            self.fillCell(cell[0], cell[1], hints[0])
            return True

        # apply n tuple
        return appyBoardObviousTuples(self, hint)

    def solveComplexity(self):
        # calculate board solving complexity
        # inspired by https://www.quora.com/How-do-they-make-Sudoku-easy-medium-or-hard-Is-it-not-just-how-many-squares-are-revealed#:~:text=Sudoku%20with%20more%20than%2019,only%20for%20very%20limited%20cells.
        # harder boards have fewer hints, easier boards have more
        # harder boards have more empty boxes
        if self.emptyCount == 0:
            return 1

        # get board's hint count - singles, doubles, triples, ...
        counts = [0]*9
        getBoardObviousSingle(self, counts)
        getBoardObviousTuples(self, counts)

        # use ratio of available obvious hints (single, double, triple) to empty cells
        # as a way to measure complexity
        return (counts[0] + counts[1] + counts[2])/self.emptyCount