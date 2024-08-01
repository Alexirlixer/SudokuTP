from cmu_graphics import *
from button import *
import time 

class PlayScreen:
    def __init__(self):
        # initialize buttons
        self.generate = Checkbox('generate', 450, 500, 'black', 'black')
        self.buttons = [ 
            LabelButton('easy', 270, 200, 'black', 'darkGreen', size = 40),
            LabelButton('medium', 270, 260, 'black', 'darkGreen', size = 40),
            LabelButton('hard', 270, 320, 'black', 'darkGreen', size = 40),
            LabelButton('expert', 270, 380, 'black', 'darkGreen', size = 40),
            LabelButton('evil', 270, 440, 'black', 'darkGreen', size = 40),
            LabelButton('back', 60, 500, 'black', 'darkGreen', size = 30),
            self.generate
            ]

def play_onAppStart(app):
    app.playScreen = PlayScreen()
   

def play_onMouseMove(app, mouseX, mouseY):
    for button in app.playScreen.buttons:
        button.mouseOver(mouseX, mouseY)


def play_onMousePress(app, mouseX, mouseY):
    for button in app.playScreen.buttons:
        if button.mouseOver(mouseX, mouseY):
            # if the back button is selected, switch the screen back to menu
            if button.text == 'back':
                app.screenSwitchSound.play()
                setActiveScreen('menu')
            elif button.text == 'generate':
                button.mousePress(mouseX, mouseY)
            else:
                # otherwise we need to select a random board of the specified
                # difficulty and then start the game
                app.screenSwitchSound.play()
                app.gameLevel = button.text
                if app.playScreen.generate.isChecked:
                        app.gameBoard = app.boardLoader.generateBoard(app.gameLevel)
                else:
                    app.gameBoard = app.boardLoader.loadBoard(app.gameLevel)
                # app.gameBoard.print()
                app.gameStart = time.time()
                setActiveScreen('game')

def play_onKeyPress(app, key):
    if key == 'up':
        onKeyUpdateButtons(app.playScreen.buttons, True)
    elif key == 'down':
        onKeyUpdateButtons(app.playScreen.buttons, False)
    elif key == 'enter':
        # same logic as for the mouse press
        for button in app.playScreen.buttons:
            if button.isSelected:
                if button.text == 'back':
                    app.screenSwitchSound.play()
                    setActiveScreen('menu')
                elif button.text == 'generate':
                    button.isChecked = not button.isChecked
                else:
                    app.screenSwitchSound.play()
                    app.gameLevel = button.text
                    if app.playScreen.generate.isChecked:
                        app.gameBoard = app.boardLoader.generateBoard(app.gameLevel)
                    else:
                        app.gameBoard = app.boardLoader.loadBoard(app.gameLevel)
                    # app.gameBoard.print()
                    app.gameStart = time.time()
                    setActiveScreen('game')
                
def play_redrawAll(app):
    # draw background
    drawImage('./media/splash.png', 0, 0, opacity=50)
    # draw Sudoku logo
    drawLabel('Sudoku', 260, 100, font='cinzel', size=80, fill='forestgreen',
        border='lightgray', borderWidth=2, opacity=60)
    # draw buttons
    for button in app.playScreen.buttons:
        button.draw()
