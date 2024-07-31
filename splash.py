from cmu_graphics import *
import time
from datetime import datetime, timedelta

def splash_onAppStart(app):
    # initializes elapsed time (may want to change this slightly)
    app.splashTime = time.time()

def splash_onStep(app):
    # this is required for the timer to work properly
    pass

def splash_redrawAll(app):
    d = timedelta(seconds=int(time.time() - app.splashTime))
    if d.seconds < 2:
        # draw background
        drawImage('./media/splash.png', 0, 0, opacity=90)
        # draw Sudoku logo and backsplash
        drawRect(120, 200, 320, 160, fill="lightgray", opacity=50)
        drawLabel('Sudoku', 280, 275, font='cinzel', size=80, fill='lightgray',
                    border='forestgreen', borderWidth=2, opacity=100)
    else:
        # switch to the menu screen after 2 seconds
        app.screenSwitchSound.play()
        setActiveScreen('menu')
        
