from cmu_graphics import *
import time 
import datetime 
from button import *

# there is a bug, when you are on a red cell -->
# (an incorrect value was entered) and you press a key that -->
# is not 1 - 9, the cell will unselect and turn -->
# grey again
# also when you click on a red cell the cell will -->
# unselect (idk if this is worth changing)
# also when you press the hint button while you have a red cell it -->
# will unselect the cell and turn grey

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
        self.hint = None
        self.legals = False
        self.buttons = [Button('back', 20, 550, 80, 50, shape='oval'),
                        Button('manual', 80, 40, 40, 40, shape = 'rect')]
        self.manualLegals = dict()
        self.manualLegalsOn = False

def game_onAppStart(app):
    app.gameScreen = GameScreen()
    
def game_onMouseMove(app, mouseX, mouseY):
    for button in app.gameScreen.buttons:
        button.color = 'white'
        if button.mouseOver(mouseX, mouseY):
            button.color = 'mediumSeaGreen'

def game_onMousePress(app, mouseX, mouseY):
    app.gameScreen.invalidOption = None
    app.gameScreen.hint = None

    for button in app.gameScreen.buttons:
        button.color = 'white'
        if button.mouseOver(mouseX, mouseY):
            button.color = 'mediumSeaGreen'
            if button.name == 'back':
                setActiveScreen('play')
            elif button.name == 'manual': 
                app.gameScreen.manualLegalsOn = not app.gameScreen.manualLegalsOn

    col = (mouseX - app.gameScreen.boardLeft) // (app.gameScreen.cellWidth)
    row = (mouseY - app.gameScreen.boardTop) // (app.gameScreen.cellHeight)
    if 0 <= col < 9 and 0 <= row < 9:
        app.gameScreen.selectedCell = (row, col)
    else:
        app.gameScreen.selectedCell = None

def game_onKeyPress(app, key):
    app.gameScreen.invalidOption = None
    # this map is for holding shift and pressing #'s
    keyMap = ['!', '@', '#', '$', '%', '^', '&', '*', '(']
    
    if '1' <= key <= '9':
        app.gameScreen.hint = None
        if app.gameScreen.selectedCell != None:
            n = int(key)
            sc = app.gameScreen.selectedCell

            if app.gameBoard.board[sc[0]][sc[1]] == 0:
                if not app.gameBoard.fillCell(sc[0], sc[1], n):
                    app.gameScreen.invalidOption = n
                else:
                    app.gameScreen.invalidOption = None
           
    elif key in keyMap:
        app.gameScreen.hint = None
        if app.gameScreen.selectedCell != None and app.gameScreen.manualLegalsOn:
            n = keyMap.index(key) + 1
            sc = app.gameScreen.selectedCell

            if sc not in app.gameScreen.manualLegals:
                app.gameScreen.manualLegals[sc] = []
            legals = app.gameScreen.manualLegals[sc]
            if n in legals:
                legals.remove(n)
            else:
                legals.append(n)

    elif key == 'left' or key == 'right' or key == 'up' or key == 'down':
        app.gameScreen.hint = None
        sc = app.gameScreen.selectedCell
        if sc == None:
            app.gameScreen.selectedCell = (0, 0)
        else:
            if key == 'left':
                if sc[1] - 1 >= 0:
                    sc = (sc[0], sc[1] - 1)
            elif key == 'right':
                if sc[1] + 1 < 9:
                    sc = (sc[0], sc[1] + 1)
            elif key == 'down':
                if sc[0] + 1 < 9:
                    sc = (sc[0] + 1, sc[1])
            elif key == 'up':
                if sc[0] - 1 >= 0:
                    sc = (sc[0] - 1, sc[1])
            app.gameScreen.selectedCell = sc
    elif key == 'h':
        app.gameScreen.hint = app.gameBoard.getHint()
    elif key == 'l':
        app.gameScreen.hint = None
        app.gameScreen.legals = not app.gameScreen.legals
    elif key == 's':
        app.gameScreen.hint = None
        app.gameBoard.solve()
    elif key == 'a': 
        if app.gameScreen.hint != None: 
            app.gameBoard.applyHint(app.gameScreen.hint)
        app.gameScreen.hint = None

# from cmu cs academy notes 6.2.3
def drawBoard(app):
    for row in range(app.gameBoard.rowCount):
        for col in range(app.gameBoard.colCount):
            drawCell(app, row, col)

# Basic function is from cmu cs academy notes 6.2.3
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

    if app.gameScreen.hint != None:
        sc = app.gameScreen.selectedCell
        for cell in app.gameScreen.hint.cells:
            if cell == (row, col):
                fillColor = 'lightBlue'
                if cell == sc:
                    fillColor = 'lightSteelBlue'

    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=fillColor, border='black',
             borderWidth=app.gameScreen.cellBorderWidth)
    
    if app.gameBoard.board[row][col] == 0:
        drawLabel(cellLabel, cellLeft + cellWidth/2, cellTop + cellHeight/2, size = 25)
        if app.gameScreen.legals == True or app.gameScreen.manualLegalsOn:
            legalWidth = cellWidth / 3
            legalHeight = cellHeight / 3 

            legals = app.gameBoard.legals[(row, col)]
            if app.gameScreen.manualLegalsOn:
                if (row, col) in app.gameScreen.manualLegals:
                    legals = app.gameScreen.manualLegals[(row, col)] 
                else:
                    legals = []
                
                    
            for i in range(3):
                for j in range(3):
                    l = ''
                    v = (i * 3) + j + 1
                    if v in legals:
                        l = str(v)
                    drawLabel(l, cellLeft + 7 + legalWidth * j, cellTop + 7
                            + legalHeight * i, size = 10, fill = 'black')
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
  offset = 3
  drawRect(app.gameScreen.boardLeft - offset, app.gameScreen.boardTop - offset, 
           app.gameScreen.boardWidth + 
           offset, app.gameScreen.boardHeight + offset,
           fill=None, border='black',
           borderWidth=3*app.gameScreen.cellBorderWidth)

def game_redrawAll(app):
    # https://stackoverflow.com/questions/775049/how-do-i-convert-seconds-to-hours-minutes-and-seconds
    elapsed = int(time.time() - app.gameStart)
    gameTime = str(datetime.timedelta(seconds=elapsed))
    drawBoard(app)
    drawBoardBorder(app)
    drawLine(137, 150, 137, 550, lineWidth = 3)
    drawLine(263, 150, 263, 550, lineWidth = 3)
    drawLine(10, 283, 390, 283, lineWidth = 3)
    drawLine(10, 417, 390, 417, lineWidth = 3)
    drawLabel(app.gameLevel, 40, 40)
    drawLabel(f"{app.gameBoard.rowCount}x{app.gameBoard.colCount}", 40, 60)
    drawLabel(gameTime, 40, 80)
    for button in app.gameScreen.buttons:
        button.draw()


