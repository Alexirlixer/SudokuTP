from cmu_graphics import *
from splash import *
from menu import *
from help import *
from play import *
from game import *
from boards.loader import FileBoardLoader 

def onAppStart(app):
    print('app starting')
    app.boardLoader = FileBoardLoader("./boards/files")

def onAppStop(app):
    print('app stopping')

def main():
    runAppWithScreens(initialScreen = 'splash', width = 400, height = 600)

main()