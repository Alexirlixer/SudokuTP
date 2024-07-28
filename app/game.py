from cmu_graphics import *
import time 
import datetime 

class GameScreen:
    def __init__(self):
        pass

def game_onAppStart(app):
    app.gameScreen = GameScreen()
    app.boardLeft = 10
    app.boardTop = 150
    app.boardWidth = 380
    app.boardHeight = 400
    app.cellBorderWidth = 1

# from cmu cs academy notes 6.2.3
def drawBoard(app):
    for row in range(app.gameBoard.rowCount):
        for col in range(app.gameBoard.colCount):
            drawCell(app, row, col)

# from cmu cs academy notes 6.2.3
def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=None, border='black',
             borderWidth=app.cellBorderWidth)
    if app.gameBoard.board[row][col] == 0:
        drawLabel('', cellLeft + cellWidth/2, cellTop + cellHeight/2, size = 16)
    else:
        s = str(app.gameBoard.board[row][col])
        drawLabel(s, cellLeft + cellWidth/2, cellTop + cellHeight/2, size = 16)


# from cmu cs academy notes 6.2.3 
def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

# from cmu cs academy notes 6.2.3
def getCellSize(app):
    cellWidth = app.boardWidth / app.gameBoard.colCount
    cellHeight = app.boardHeight / app.gameBoard.rowCount
    return (cellWidth, cellHeight)

# from cmu cs academy notes 6.2.3
def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=5*app.cellBorderWidth)

def game_redrawAll(app):
    # https://stackoverflow.com/questions/775049/how-do-i-convert-seconds-to-hours-minutes-and-seconds
    elapsed = int(time.time() - app.gameStart)
    gameTime = str(datetime.timedelta(seconds=elapsed))
    drawBoard(app)
    drawBoardBorder(app)
    drawLine(137, 150, 137, 550, lineWidth = 5)
    drawLine(263, 150, 263, 550, lineWidth = 5)
    drawLine(10, 283, 390, 283, lineWidth = 5)
    drawLine(10, 417, 390, 417, lineWidth = 5)
    drawLabel(app.gameLevel, 40, 40)
    drawLabel(f"{app.gameBoard.rowCount}x{app.gameBoard.colCount}", 40, 60)
    drawLabel(gameTime, 40, 80)


    # for i in range(app.gameBoard.rowCount):
    #     for j in range(app.gameBoard.colCount):
    #         v = app.gameBoard.board[i][j]
    #         l = str(v)
    #         if v == 0:
    #             l = ' '

    #         drawLabel(l, 40*i, 60 + 40*j)