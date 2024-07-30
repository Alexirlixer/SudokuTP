from cmu_graphics import *
from button import *
import time 

class PlayScreen:
    def __init__(self):
        # self.buttons = [
        #     Button('easy', 150, 275, 100, 50),
        #     Button('medium', 150, 330, 100, 50),
        #     Button('hard', 150, 385, 100, 50),
        #     Button('expert', 150, 440, 100, 50),
        #     Button('evil', 150, 495, 100, 50),
        #     Button('back', 40, 520, 80, 50, shape='oval'),
        # ]
        self.buttons = [ 
            LabelButton('easy', 270, 200, 'black', 'darkGreen', size = 40),
            LabelButton('medium', 270, 260, 'black', 'darkGreen', size = 40),
            LabelButton('hard', 270, 320, 'black', 'darkGreen', size = 40),
            LabelButton('expert', 270, 380, 'black', 'darkGreen', size = 40),
            LabelButton('evil', 270, 440, 'black', 'darkGreen', size = 40),
            LabelButton('back', 60, 500, 'black', 'darkGreen', size = 30)
            ]

def play_onAppStart(app):
    app.playScreen = PlayScreen()
   

def play_onMouseMove(app, mouseX, mouseY):
    for button in app.playScreen.buttons:
        button.mouseOver(mouseX, mouseY)


def play_onMousePress(app, mouseX, mouseY):
    for button in app.playScreen.buttons:
        if button.mouseOver(mouseX, mouseY):
            if button.text == 'back':
                app.screenSwitchSound.play()
                setActiveScreen('menu')
            else:
                app.screenSwitchSound.play()
                app.gameLevel = button.text
                app.gameBoard = app.boardLoader.loadBoard(app.gameLevel)
                app.gameStart = time.time()
                setActiveScreen('game')

def play_onKeyPress(app, key):
    if key == 'up':
        onKeyUpdateButtons(app.playScreen.buttons, True)
    elif key == 'down':
        onKeyUpdateButtons(app.playScreen.buttons, False)
    elif key == 'enter':
        for button in app.playScreen.buttons:
            if button.isSelected:
                if button.text == 'back':
                    app.screenSwitchSound.play()
                    setActiveScreen('menu')
                else:
                    app.screenSwitchSound.play()
                    app.gameLevel = button.text
                    app.gameBoard = app.boardLoader.loadBoard(app.gameLevel)
                    app.gameStart = time.time()
                    setActiveScreen('game')
            

    # for button in app.playScreen.buttons:
    #     button.color = 'white'
    #     if button.mouseOver(mouseX, mouseY):
    #         button.color = 'mediumSeaGreen'
    #         if button.name == 'back':
    #             setActiveScreen('menu')
    #         else:
    #             app.gameLevel = button.name
    #             app.gameBoard = app.boardLoader.loadBoard(app.gameLevel)
    #             app.gameStart = time.time()
    #             setActiveScreen('game')
            
def play_redrawAll(app):
    # maybe get rid of this rect code, it just draws a border around the screen
    drawImage('./media/splash.png', 0, 0, opacity=50)
    drawLabel('Sudoku', 260, 100, font='cinzel', size=80, fill='forestgreen',
        border='lightgray', borderWidth=2, opacity=60)
    for button in app.playScreen.buttons:
        button.draw()
    # drawLabel('Select Difficulty', 200, 200, size = 30)
