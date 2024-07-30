from cmu_graphics import *
from splash import *
from menu import *
from help import *
from play import *
from game import *
from boards.loader import FileBoardLoader 
from boards.hints import *

def onAppStart(app):
    print('app starting')
    app.boardLoader = FileBoardLoader("./boards/files")

def onAppStop(app):
    print('app stopping')

# def onStep(app):
#     pass

def main():
    runAppWithScreens(initialScreen = 'splash', width = 520, height = 570)


main()