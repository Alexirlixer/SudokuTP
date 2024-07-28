from cmu_graphics import *
from button import *
import time 

class PlayScreen:
    def __init__(self):
        self.buttons = [
            Button('easy', 150, 275, 100, 50),
            Button('medium', 150, 330, 100, 50),
            Button('hard', 150, 385, 100, 50),
            Button('expert', 150, 440, 100, 50),
            Button('evil', 150, 495, 100, 50),
            Button('back', 40, 520, 80, 50, shape='oval'),
        ]

def play_onAppStart(app):
    app.playScreen = PlayScreen()
   

def play_onMouseMove(app, mouseX, mouseY):
    for button in app.playScreen.buttons:
        button.color = 'white'
        if button.mouseOver(mouseX, mouseY):
            button.color = 'mediumSeaGreen'


def play_onMousePress(app, mouseX, mouseY):
    for button in app.playScreen.buttons:
        button.color = 'white'
        if button.mouseOver(mouseX, mouseY):
            button.color = 'mediumSeaGreen'
            if button.name == 'back':
                setActiveScreen('menu')
            else:
                app.gameLevel = button.name
                app.gameBoard = app.boardLoader.loadBoard(app.gameLevel)
                app.gameStart = time.time()
                setActiveScreen('game')
            
def play_redrawAll(app):
    # maybe get rid of this rect code, it just draws a border around the screen
    drawRect(0, 0, 400, 600, fill = None, border = 'black', borderWidth = 10)
    drawLabel('Sudoku', 200, 100, size = 85)
    drawLabel('Select Difficulty', 200, 200, size = 30)
    for button in app.playScreen.buttons:
        button.draw()
