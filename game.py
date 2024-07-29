from cmu_graphics import *
import time 
import datetime 

class GameScreen:
    def __init__(self):
        self.boardLeft = 10
        self.boardTop = 150
        self.boardWidth = 380
        self.boardHeight = 400
        self.cellBorderWidth = 1
        self.cellWidth = self.boardWidth // 9
        self.cellHeight = self.boardHeight // 9
        self.selectedCell = None
        self.invalidOption = None

def game_onAppStart(app):
    app.gameScreen = GameScreen()
    

def game_onMousePress(app, mouseX, mouseY):
    app.gameScreen.invalidOption = None
    col = (mouseX - app.gameScreen.boardLeft) // (app.gameScreen.cellWidth)
    row = (mouseY - app.gameScreen.boardTop) // (app.gameScreen.cellHeight)
    if 0 <= col < 9 and 0 <= row < 9:
        app.gameScreen.selectedCell = (row, col)
    else:
        app.gameScreen.selectedCell = None

def game_onKeyPress(app, key):
    if app.gameScreen.selectedCell != None:
        if '1' <= key <= '9':
            n = int(key)
            sc = app.gameScreen.selectedCell
            if app.gameBoard.board[sc[0]][sc[1]] == 0:
                if not app.gameBoard.fillCell(sc[0], sc[1], n):
                    app.gameScreen.invalidOption = n
                else:
                    app.gameScreen.invalidOption = None

# from cmu cs academy notes 6.2.3
def drawBoard(app):
    for row in range(app.gameBoard.rowCount):
        for col in range(app.gameBoard.colCount):
            drawCell(app, row, col)

# from cmu cs academy notes 6.2.3
def drawCell(app, row, col):
    cellLabel = ''
    fillColor = None
    if app.gameScreen.selectedCell == (row, col):
        if app.gameScreen.invalidOption != None:
            cellLabel = str(app.gameScreen.invalidOption)
            fillColor = 'red'
        else:
            fillColor = 'grey'

    elif app.gameScreen.selectedCell != None:
        sc = app.gameScreen.selectedCell
        rowBlockStart = sc[0] // 3 * 3
        colBlockStart = sc[1] // 3 * 3

        if (row == sc[0] or col == sc[1] or 
            (rowBlockStart <= row < rowBlockStart + 3 and 
             colBlockStart <= col < colBlockStart + 3)):
            fillColor = 'lightGrey'
        
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=fillColor, border='black',
             borderWidth=app.gameScreen.cellBorderWidth)
    
    if app.gameBoard.board[row][col] == 0:
        drawLabel(cellLabel, cellLeft + cellWidth/2, cellTop + cellHeight/2, size = 25)
    else:
        s = str(app.gameBoard.board[row][col])
        drawLabel(s, cellLeft + cellWidth/2, cellTop + cellHeight/2, size = 25)


# from cmu cs academy notes 6.2.3 
def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.gameScreen.boardLeft + col * cellWidth
    cellTop = app.gameScreen.boardTop + row * cellHeight
    return (cellLeft, cellTop)

# from cmu cs academy notes 6.2.3
def getCellSize(app):
    cellWidth = app.gameScreen.boardWidth / app.gameBoard.colCount
    cellHeight = app.gameScreen.boardHeight / app.gameBoard.rowCount
    return (cellWidth, cellHeight)

# from cmu cs academy notes 6.2.3
def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.gameScreen.boardLeft, app.gameScreen.boardTop, app.gameScreen.boardWidth, app.gameScreen.boardHeight,
           fill=None, border='black',
           borderWidth=5*app.gameScreen.cellBorderWidth)

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


