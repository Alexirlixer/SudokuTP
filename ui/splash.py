from cmu_graphics import *
import time

def splash_onAppStart(app):
    pass

def splash_onMousePress(app, mouseX, mouseY):
    setActiveScreen('menu')

def splash_redrawAll(app):
    drawLabel('Sudoku', 200, 100, size = 85)
    drawLabel('- AA', 200, 300, size = 40)

    # how to make it go away by itself in 3 seconds
    # how to make it fade in and out

