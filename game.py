from cmu_graphics import *
import time 
import datetime 
from button import *
import copy
from boards.board import Board

class GameScreen:
    def __init__(self):
        # initialize all of the requirements for the board to be drawn
        self.boardLeft = 70
        self.boardTop = 90
        self.boardWidth = 380
        self.boardHeight = 400
        self.cellBorderWidth = 1
        self.cellWidth = self.boardWidth // 9
        self.cellHeight = self.boardHeight // 9
        self.selectedCell = None
        self.invalidOption = None
        self.hint = None
        self.autoLegalsOn = False
        self.checkBoxAutoLegals = Checkbox('auto', 480, 530, 'black', 'black')
        self.checkBoxManualLegals = Checkbox('manual', 400, 530, 'black', 'black')
        self.buttons = [LabelButton('back', 50, 520, 'black', 'black', size = 20),
                        self.checkBoxManualLegals,
                        self.checkBoxAutoLegals
                        ]
        self.manualLegals = dict()
        self.manualLegalsOn = False
        self.timer = TimerLabel('Elapsed', 440, 50)

def game_onAppStart(app):
    app.gameScreen = GameScreen()
    
def game_onMouseMove(app, mouseX, mouseY):
    for button in app.gameScreen.buttons:
        button.mouseOver(mouseX, mouseY)

def game_onMousePress(app, mouseX, mouseY):
    # if the board is completed then allow the user to click the mouse
    # to return to the play screen
    if app.gameBoard.isSolved():
        setActiveScreen('play')
        return

    app.gameScreen.invalidOption = None
    app.gameScreen.hint = None

    for button in app.gameScreen.buttons:
        button.mousePress(mouseX, mouseY)
        if button.isSelected:
            if button.text == 'back':
                app.screenSwitchSound.play()
                setActiveScreen('play')
            # if manual mode is selected disable auto mode for legals
            elif button.text == 'manual': 
                app.gameScreen.manualLegalsOn = button.isChecked
                app.gameScreen.autoLegalsOn = False
                app.gameScreen.checkBoxAutoLegals.isChecked = False
            # if auto mode is selected disable manual mode for legals
            elif button.text == 'auto':
                app.gameScreen.manualLegalsOn = False
                app.gameScreen.autoLegalsOn = button.isChecked
                app.gameScreen.checkBoxManualLegals.isChecked = False

    # determine which col and which row the user has clicked in
    col = (mouseX - app.gameScreen.boardLeft) // (app.gameScreen.cellWidth)
    row = (mouseY - app.gameScreen.boardTop) // (app.gameScreen.cellHeight)
    # if the user clicked within the board set the selected cell to their click
    if 0 <= col < 9 and 0 <= row < 9:
        app.gameScreen.selectedCell = (row, col)
    # other wise there should be no selected cell
    else:
        app.gameScreen.selectedCell = None

def game_onKeyPress(app, key):
    # when the board is solved allow the user to press 'r' to return to the
    # play screen
    if app.gameBoard.isSolved():
        if key == 'r':
            setActiveScreen('play')
        return
    
    app.gameScreen.invalidOption = None
    # this map is for holding shift and pressing #'s
    keyMap = ['!', '@', '#', '$', '%', '^', '&', '*', '(']
    
    # make sure the user selected a digit 1 - 9
    if '1' <= key <= '9':
        app.gameScreen.hint = None
        # make sure there is a selected cell
        if app.gameScreen.selectedCell != None:
            # set the key to an integer value of the selected key
            n = int(key)
            sc = app.gameScreen.selectedCell

            # check that the selected cell is empty
            if app.gameBoard.board[sc[0]][sc[1]] == 0:
                # check that the cell can be filled
                if not app.gameBoard.fillCell(sc[0], sc[1], n):
                    app.gameScreen.invalidOption = n
                else:
                    # verify that this valid value will not lead to an 
                    # unsolvable game in the future
                    test = Board(copy.deepcopy(app.gameBoard.board))
                    if not test.solve():
                        app.gameScreen.invalidOption = n
                        app.gameBoard.emptyCell(sc[0], sc[1])
                    else:
                        app.gameScreen.invalidOption = None

    # the user shift toggled their #'s
    elif key in keyMap:
        app.gameScreen.hint = None
        # make sure there is a selected cell and manual legal mode is on
        if app.gameScreen.selectedCell != None and app.gameScreen.manualLegalsOn:
            n = keyMap.index(key) + 1
            sc = app.gameScreen.selectedCell

            # check if selected cell is in the legal dict
            if sc not in app.gameScreen.manualLegals:
                app.gameScreen.manualLegals[sc] = []
            legals = app.gameScreen.manualLegals[sc]
            # remove the number if it is in legals
            if n in legals:
                legals.remove(n)
            else:
                legals.append(n)

    elif key == 'left' or key == 'right' or key == 'up' or key == 'down':
        # if key == 'up':
        #     onKeyUpdateButtons(app.gameScreen.buttons, True)
        # elif key == 'down':
        #     onKeyUpdateButtons(app.gameScreen.buttons, False)
        app.gameScreen.hint = None
        sc = app.gameScreen.selectedCell
        # initialize a selected cell on an intial arrow key press
        if sc == None:
            app.gameScreen.selectedCell = (0, 0)
        else:
            # logic for shifting selected cell
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
    # get hints
    elif key == 'h':
        app.gameScreen.hint = app.gameBoard.getHint()
    # display legals
    elif key == 'l':
        app.gameScreen.hint = None
        app.gameScreen.autoLegalsOn = not app.gameScreen.autoLegalsOn
        app.gameScreen.manualLegalsOn = False
        for button in app.gameScreen.buttons:
            if button.text == 'auto':
                button.isChecked = app.gameScreen.autoLegalsOn
                app.gameScreen.checkBoxManualLegals.isChecked = False
                break
    elif key == 'm':
        app.gameScreen.hint = None
        app.gameScreen.autoLegalsOn = False
        app.gameScreen.manualLegalsOn = not app.gameScreen.manualLegalsOn
        for button in app.gameScreen.buttons:
            if button.text == 'manual':
                button.isChecked = app.gameScreen.manualLegalsOn
                app.gameScreen.checkBoxAutoLegals.isChecked = False
                break 
    # solve the board
    elif key == 's':
        app.gameScreen.hint = None
        app.gameBoard.solve()
    # apply hints
    elif key == 'a': 
        if app.gameScreen.hint != None: 
            app.gameBoard.applyHint(app.gameScreen.hint)
        app.gameScreen.hint = None
    # select button with 'enter' key
    # elif key == 'enter':
    #     for button in app.gameScreen.buttons:
    #         if button.isSelected:
    #             if type(button) == Checkbox:
    #                 button.isChecked = not button.isChecked
    #             elif type(button) == LabelButton:
    #                 pass
    elif key == 'b':
        app.screenSwitchSound.play()
        setActiveScreen('play')
    elif key == 'x':
        hint = app.gameBoard.getHint()
        while hint != None:
            if hint.region != 'cell':
                break
            else:
                app.gameBoard.applyHint(hint)
            hint = app.gameBoard.getHint()  


# from cmu cs academy notes 6.2.3
def drawBoard(app):
    s = app.gameScreen
    drawRect(s.boardLeft, s.boardTop, s.boardWidth, s.boardHeight, fill = 
             'white', opacity = 80)
    for row in range(app.gameBoard.rowCount):
        for col in range(app.gameBoard.colCount):
            drawCell(app, row, col)

# Basic function is from cmu cs academy notes 6.2.3
# with changes made to accomodate drawing values
def drawCell(app, row, col):
    cellLabel = ''
    fillColor = None
    if app.gameScreen.selectedCell == (row, col):
        # if an invalid option was entered make the cell red
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

    # make the hint color light blue if its not the selected cell, other wise
    # make it a slightly darker blue
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
    
    # check cell empty
    if app.gameBoard.board[row][col] == 0:
        drawLabel(cellLabel, cellLeft + cellWidth/2, cellTop + cellHeight/2, 
                  size = 25)
        if app.gameScreen.autoLegalsOn == True or app.gameScreen.manualLegalsOn:
            legalWidth = cellWidth / 3
            legalHeight = cellHeight / 3 

            legals = app.gameBoard.legals[(row, col)]
            if app.gameScreen.manualLegalsOn:
                if (row, col) in app.gameScreen.manualLegals:
                    legals = app.gameScreen.manualLegals[(row, col)] 
                else:
                    legals = []
                
            
            # draw legals
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
  # draw the board outline (with triple-thickness):
  offset = 3
  drawRect(app.gameScreen.boardLeft - offset, app.gameScreen.boardTop - offset, 
           app.gameScreen.boardWidth + 
           offset, app.gameScreen.boardHeight + offset,
           fill=None, border='black',
           borderWidth=3*app.gameScreen.cellBorderWidth)

def game_redrawAll(app):
    # draw background
    drawImage('./media/splash.png', 0, 0, opacity=60)
    drawBoard(app)
    drawBoardBorder(app)
    s = app.gameScreen
    # draw block dividers
    drawLine(s.boardLeft, s.boardTop + s.cellHeight * 3, s.boardLeft + s.boardWidth,
             s.boardTop + s.cellHeight * 3, lineWidth = 3)
    drawLine(s.boardLeft, s.boardTop + s.cellHeight * 6, s.boardLeft + s.boardWidth,
             s.boardTop + s.cellHeight * 6, lineWidth = 3)
    drawLine(s.boardLeft + s.cellWidth * 3, s.boardTop, 
              s.boardLeft + s.cellWidth * 3, s.boardTop + s.boardHeight, 
              lineWidth = 3)
    drawLine(s.boardLeft + s.cellWidth * 6, s.boardTop, 
              s.boardLeft + s.cellWidth * 6, s.boardTop + s.boardHeight, 
              lineWidth = 3)

    app.gameScreen.timer.draw()
    drawLabel(f'Level: {app.gameLevel.capitalize()}', 100, 50, font = 'cinzel',
              fill = 'black', size = 17, opacity = 60)

    for button in app.gameScreen.buttons:
        button.draw()

    drawLabel('Legals', 385, 500, font='cinzel',
                  size=17, fill='black', border='black', borderWidth=0,
                  opacity=60)
    
    # display 'game over' if board is solved
    if app.gameBoard.isSolved():
        drawRect(60, 200, 440, 160, fill="lightgray", opacity=80)
        drawLabel('Game Over', 280, 275, font='cinzel', size=80, fill='lightgray',
                    border='forestgreen', borderWidth=2, opacity=100)
