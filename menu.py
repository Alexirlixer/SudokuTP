from cmu_graphics import *
from button import *

class MenuScreen:
    def __init__(self):
        self.buttons = [
            LabelButton('play', 270, 230, 'black', 'forestgreen'),
            LabelButton('help', 270, 330, 'black', 'forestgreen')
            ]
        self.selected = 0
        

def menu_onAppStart(app):
    app.menuScreen = MenuScreen()
    app.menuScreen.buttons[0].isSelected = True

def menu_onKeyPress(app, key):
    if key == 'up':
        onKeyUpdateButtons(app.menuScreen.buttons, True)
    elif key == 'down':
        onKeyUpdateButtons(app.menuScreen.buttons, False)
    elif key == 'enter':
        for button in app.menuScreen.buttons:
            if button.isSelected:
                app.screenSwitchSound.play()
                setActiveScreen(button.text)


    # if key == 'up':
    #     for i in range(len(app.menuScreen.buttons)):
    #         if app.menuScreen.buttons[i].isSelected:
    #             if i + 1 < len(app.menuScreen.buttons):
    #                 app.menuScreen.buttons[i].isSelected = False
    #                 app.menuScreen.buttons[i + 1].isSelected = True
    #             else:
    #                 app.menuScreen.buttons[i].isSelected = False
    #                 app.menuScreen.buttons[0].isSelected = True
    # elif key == 'down':
    #     for i in range(len(app.menuScreen.buttons)):
    #         if app.menuScreen.buttons[i].isSelected:
    #             if i - 1 >= 0:
    #                 app.menuScreen.buttons[i].isSelected = False
    #                 app.menuScreen.buttons[i - 1].isSelected = True
    #             else:
    #                 app.menuScreen.buttons[i].isSelected = False
    #                 app.menuScreen.buttons[-1].isSelected = True
    # elif key == 'enter':
    #     for button in app.menuScreen.buttons:
    #         if button.isSelected:
    #             app.screenSwitchSound.play()
    #             setActiveScreen(button.text)
               

def menu_onMouseMove(app, mouseX, mouseY):
    for button in app.menuScreen.buttons:
        button.mouseOver(mouseX, mouseY)

def menu_onMousePress(app, mouseX, mouseY):
    for button in app.menuScreen.buttons:
        if button.mouseOver(mouseX, mouseY):
            app.screenSwitchSound.play()
            setActiveScreen(button.text)

def menu_redrawAll(app):
    drawImage('./media/splash.png', 0, 0, opacity=50)
    drawLabel('Sudoku', 260, 100, font='cinzel', size=80, fill='forestgreen',
                border='lightgray', borderWidth=2, opacity=60)
    for button in app.menuScreen.buttons:
        button.draw()
