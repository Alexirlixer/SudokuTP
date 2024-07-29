import itertools


class Hint:
    def __init__(self, region, cells):
        # region can be:
        # - cell for single
        # - row for tuples extracted from a single row
        # - col for tuples extracted from a single col
        # - block for tuples extracted from a block
        self.region = region
        self.cells = cells


def getBoardObviousSingle(board):
    for cell, legals in board.legals.items():
        if len(legals) == 1:
            return Hint('cell', [cell])

    return None


def getRegionEmptyCells(board, row=-1, col=-1):
    # get region cells which have not been completed yet
    # row = row to use, col = col to use
    # either one or both have to be specified
    if row == -1 and col == -1:
        return None

    rowBlockStart = row // 3 * 3
    colBlockStart = col // 3 * 3

    cells = set()

    # collect all cells with legal candidates from the region
    # we're interested in
    for cell, legals in board.legals.items():
        if row == -1:
            # only col set
            if cell[1] == col:
                cells.add(cell)
        elif col == -1:
            # only row set
            if cell[0] == row:
                cells.add(cell)
        else:
            # match block
            if ((rowBlockStart <= cell[0] < rowBlockStart + 3) and
                    (colBlockStart <= cell[1] < colBlockStart + 3)):
                cells.add(cell)

    return cells


def getCellsLegals(board, cells):
    # get all legals for a cells list
    legals = set()

    for cell in cells:
        legals.update(board.legals[cell])

    return legals


def getRegionObviousTuples(board, row=-1, col=-1):
    cells = getRegionEmptyCells(board, row, col)
    if cells == None:
        return None

    # check for obvious doubles and triples
    for i in range(2, 4):
        for o in itertools.combinations(cells, i):
            legals = getCellsLegals(board, o)
            if len(legals) == i:
                return o

    return None


def getBoardObviousTuples(board):
    # see https://sudoku.com/sudoku-rules/obvious-pairs/
    # see https://sudoku.com/sudoku-rules/obvious-triples/
    blockSize = 3

    # check each block
    for i in range(0, board.rowCount, blockSize):
        for j in range(0, board.colCount, blockSize):
            tuples = getRegionObviousTuples(board, row=i, col=j)
            if tuples != None:
                return Hint('block', tuples)

    # check each row
    for i in range(board.rowCount):
        tuples = getRegionObviousTuples(board, row=i)
        if tuples != None:
            return Hint('row', tuples)

    # check each column
    for j in range(board.colCount):
        tuples = getRegionObviousTuples(board, col=j)
        if tuples != None:
            return Hint('col', tuples)

    return None


def appyBoardObviousTuples(board, hint):
    # collect all empty cells from the same region
    if hint.region == 'row':
        cell = hint.cells[0]
        affectedCells = getRegionEmptyCells(board, row=cell[0])
    elif hint.region == 'col':
        cell = hint.cells[0]
        affectedCells = getRegionEmptyCells(board, col=cell[1])
    else:
        cell = hint.cells[0]
        affectedCells = getRegionEmptyCells(board, row=cell[0], col=cell[1])
    if affectedCells == None:
        return False

    # remove from this list the cells which are part of the hint
    # so we are left only with the empty cells for which legals
    # need to be updated
    for cell in hint.cells:
        affectedCells.remove(cell)

    # collect union of legals from the hint so we can remove them
    # from cells that need to be updated
    hintLegals = getCellsLegals(board, hint.cells)

    # update legals
    for cell in affectedCells:
        # get affected cell legals and remove from them anything
        # that is part of the hint
        cellLegals = board.legals[cell]
        for l in hintLegals:
            if l in cellLegals:
                cellLegals.remove(l)

        # update the current legals for the cell
        board.legals[cell] = cellLegals