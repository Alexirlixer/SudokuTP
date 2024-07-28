from cmu_graphics import *
from ui.splash import foo

foo()

def onAppStart(app):
    app.rows = 9
    app.cols = 9
    app.boardLeft = 20
    app.boardTop = 20
    app.boardWidth = 300
    app.boardHeight = 300
    app.cellBorderWidth = 2

# Lines 8 - 11 are from the cs academy 6.2.3 notes
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

# Lines 14 - 19 are from the cs academy 6.2.3 notes
def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=None, border='black',
             borderWidth=app.cellBorderWidth)

# Lines 22 - 26 are from the cs academy 6.2.3 notes
def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

# Lines 29 - 32 are from the cs academy 6.2.3 notes
def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

# Lines 35 - 38 are from the cs academy 6.2.3 notes
def drawBoardBorder(app):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

def redrawAll(app):
    drawBoard(app)

runApp()