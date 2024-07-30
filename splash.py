from cmu_graphics import *
import time
from datetime import datetime, timedelta

def splash_onAppStart(app):
    app.splashTime = time.time()


def splash_onMousePress(app, mouseX, mouseY):
    setActiveScreen('menu')

def splash_onStep(app):
    pass

def splash_redrawAll(app):
    d = timedelta(seconds=int(time.time() - app.splashTime))
    if d.seconds < 3:
        drawImage('./media/splash.png', 0, 0, opacity=90)
        drawRect(120, 200, 320, 160, fill="lightgray", opacity=50)
        drawLabel('Sudoku', 280, 275, font='cinzel', size=80, fill='lightgray',
                    border='forestgreen', borderWidth=2, opacity=100)
    else:
        setActiveScreen('menu')
        
