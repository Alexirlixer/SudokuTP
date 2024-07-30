import os
import random

from boards.board import Board


class BoardLoader(object):
    def __init__(self):
        pass

    def loadBoard(self, level):
        return None


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


class FileBoardLoader(BoardLoader):
    def __init__(self, folder):
        self.folder = folder

        boards = {
            'easy': [],
            'medium': [],
            'hard': [],
            'expert': [],
            'evil' : []
        }

        for filename in os.listdir(self.folder):
            if filename.endswith(".txt"):
                level = filename.split('-')[0]

                board = loadBoardFile(f'{self.folder}/{filename}')
                if board != None:
                    boards[level].append(board)

        self.boards = boards

    def loadBoard(self, level):
        if level not in self.boards:
            return None

        boards = self.boards[level]
        i = random.randint(0, len(boards) - 1)
        return Board(boards[i])