import copy
import os
import random
import statistics

from boards.board import Board


def readFile(filename):
    with open(filename, "rt") as f:
        return f.read()


def loadBoardFile(filename):
    data = readFile(filename)

    board = []

    lines = data.split('\n')
    for line in lines:
        row = line.split(' ')
        board.append([int(c) for c in row])

    return board


# https://pi.math.cornell.edu/~mec/Summer2009/Mahmood/Symmetry.html
def relabelDigits(board):
    # swap game digits
    rowCount = len(board)
    colCount = len(board[0])

    # create relabel list
    # https://www.geeksforgeeks.org/random-shuffle-function-in-python/
    # create the relabel list, number "i" will be replaced by relabel[i]
    relabel = [i for i in range(1, 10)]
    random.shuffle(relabel)

    for i in range(rowCount):
        for j in range(colCount):
            n = board[i][j] - 1
            board[i][j] = relabel[n]

# https://pi.math.cornell.edu/~mec/Summer2009/Mahmood/Symmetry.html
def permuteBandRows(board):
    # swap rows in bands
    rowCount = len(board)

    # create row permutations, row "i" will be replaced by row p[i]
    p = [i for i in range(0, 3)]
    random.shuffle(p)

    rows = []

    # for every band
    for i in range(0, rowCount, 3):
        # add rows in the permutation order
        for j in range(len(p)):
            rows.append(board[i + p[j]])

    return rows

# https://pi.math.cornell.edu/~mec/Summer2009/Mahmood/Symmetry.html
def permuteStackCols(board):
    # swap columns in stack
    rowCount = len(board)
    colCount = len(board[0])

    # create col permutations, col "i" will be replaced by col p[i]
    p = [i for i in range(0, 3)]
    random.shuffle(p)

    newBoard = [[0] * colCount for i in range(rowCount)]

    # for every stack
    for j in range(0, colCount, 3):
        for i in range(rowCount):
            for k in range(len(p)):
                newColumn = p[k]
                newBoard[i][j + k] = board[i][j + newColumn]

    return newBoard

def generateBoardComplexityWrapper(board, complexity):
    # backtracking based  algorithm to generate a board with a given complexity
    # keep removing cells until we reach the desired level of complexity
    # make sure we do not return a solved board
    if not board.isSolved():
        # if current board complexity is one std dev away from mean we're done
        c = board.solveComplexity()
        if c <= complexity[0] + complexity[1]:
            # check if complexity is in the desired range
            if complexity[0] - complexity[1] <= c:
                return True
            else:
                # too complex - backtrack
                return False

    # use random cell positions otherwise boards will
    # have all set numbers in the bottom right corner
    # https://www.w3schools.com/python/ref_random_shuffle.asp
    positions = [i for i in range(0, 9)]
    random.shuffle(positions)

    for row in positions:
        for col in positions:
            v = board.board[row][col]
            if v == 0:
                continue

            # remove the value and check the rest
            board.emptyCell(row, col)
            if generateBoardComplexityWrapper(board, complexity):
                return True

            # previous cell did not result in a good board
            # reset and use the next one
            board.fillCell(row, col, v)

    return False

def boardsLevelComplexity(boards):
    # get complexities of all boards at this level
    complexity = []
    for i in range(len(boards)):
        board = Board(boards[i])
        complexity.append(board.solveComplexity())

    # calculate mean and std dev required for a game to be at this level
    return statistics.mean(complexity), statistics.stdev(complexity)


class FileBoardLoader:
    def __init__(self, folder):
        self.folder = folder

        boards = {
            'easy': [],
            'medium': [],
            'hard': [],
            'expert': [],
            'evil': []
        }

        for filename in os.listdir(self.folder):
            if filename.endswith(".txt"):
                level = filename.split('-')[0]

                board = loadBoardFile(f'{self.folder}/{filename}')
                if board != None:
                    boards[level].append(board)

        self.boards = boards

        # calculate level complexity using all the loaded boards
        # this will calculate, for each level, (mean, std dev) a
        # board complexity needs to fall into to be at that level
        levelComplexity = {}
        for level in boards.keys():
            mean, stddev = boardsLevelComplexity(self.boards[level])

            if stddev <= 0:
                # standard deviation cannot be zero, make it something small
                stddev = 0.02
            if mean + stddev >= 1:
                # mean to std dev is greater than one - this will result in super
                # easy puzzles. make it slightly harder, make mean = 0.90 - stddev
                # to ensure there are at least a couple of hints and empty cells
                mean = 0.90 - stddev

            levelComplexity[level] = (mean, stddev)

        self.levelComplexity = levelComplexity
        #print(levelComplexity)

    def loadBoard(self, level):
        if level not in self.boards:
            return None

        boards = self.boards[level]
        i = random.randint(0, len(boards) - 1)
        return Board(copy.deepcopy(boards[i]))

    def randomBoard(self, level):
        # generate a new random board
        # - select a random board for this level
        # - mix the board using symmetry rules
        # - zero out the original cells to make the new board match
        # the original level
        if level not in self.boards:
            return None

        # choose a random board from the same level
        levelBoards = self.boards[level]
        i = random.randint(0, len(levelBoards)-1)
        initialBoard = levelBoards[i]

        # create a board with this random game and solve it
        solvedBoard = Board(copy.deepcopy(initialBoard))
        #solvedBoard.print()
        if not solvedBoard.solve():
            return None

        # shuffle solved board using symmetry rules
        # https://www.geeksforgeeks.org/random-shuffle-function-in-python/
        randomBoard = solvedBoard.board

        for i in range(random.randint(3, 10)):
            relabelDigits(randomBoard)
            randomBoard = permuteBandRows(randomBoard)
            randomBoard = permuteStackCols(randomBoard)

        # copy over the zeroes from the original board to the new
        # randomized one - this should result in a valid, solvable
        # board since all the transformations are symmetric
        for i in range(len(randomBoard)):
            for j in range(len(randomBoard[0])):
                if initialBoard[i][j] == 0:
                    randomBoard[i][j] = 0

        return Board(randomBoard)
    def generateBoard(self, level):
        # generate a new board
        # - select a solvable board from any level
        # - solve the board
        # - randomize the board using symmetry rules
        # - using the pre-calculated distributions for the level
        # and backtracking generate a new unsolved board with the
        # complexity in the (mean, std dev) range
        if level not in self.boards:
            return None

        # choose a random level to use as starting point
        levels = [l for l in self.boards.keys()]
        i = random.randint(0, len(levels)-1)
        randomLevel = levels[i]

        # choose a random game from that level
        randomBoards = self.boards[randomLevel]
        j = random.randint(0, len(randomBoards)-1)
        randomBoard = randomBoards[j]

        # create a board with this random game and solve it
        solvedBoard = Board(copy.deepcopy(randomBoard))
        if not solvedBoard.solve():
            return None

        # shuffle solved board using symmetry rules
        # https://www.geeksforgeeks.org/random-shuffle-function-in-python/
        randomBoard = solvedBoard.board

        for i in range(random.randint(3, 10)):
            relabelDigits(randomBoard)
            randomBoard = permuteBandRows(randomBoard)
            randomBoard = permuteStackCols(randomBoard)

        # make a new game using randomized solved
        board = Board(randomBoard)

        complexity = self.levelComplexity[level]
        if generateBoardComplexityWrapper(board, complexity):
            return board

        return None

if __name__ == "__main__":
    loader = FileBoardLoader("./files/boards")

    for level in loader.boards.keys():
        board = loader.generateBoard(level)
        print(level, board.solveComplexity())
        board.print()
        # print('solved', board.solve())
        # board.print()