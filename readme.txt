This project was created for the 15-112 summer 2024 semester, and is a fully
working version of Sudoku.
App Features:
    - Runs offline using the desktop-installed version of cs academy
    - Screens: splash, menu, help, play, and game screens
    - Randomly loads hardcoaded boards from text files by type
    - Randomly transforms boards based on the level
    - Generates random boards based on selected level
    - Keyboard only and Mouse only modes
    - Automatic and manual modes for legal values (user needs to toggle shift
      and enter values in order to update the boards legals on manual mode; on
      auto mode the board will do this for the user)
    - Incorrect value indicator (cell turns red when incorrect value is entered)
    - Backtracking solver (solves board) (with optimizations)
    - Simple and complex hints: obvious singles and obvious tuples
    - Hint indication
    - Getting and applying hints (with optimizations)
    - Autoplayed singletons

How to run:
    - Copy the code into a folder
    - Install cmu graphics and required dependencies
    - Go to folder and run python runui.py

Controls for key board and mouse only modes:
    Keyboard
    - use arrows to navigate and enter to select
    - 1..9 keys to enter number in selected cell
    - h to show hint, a to apply hint, x to apply singletons
    - s to solve, l for auto legals
    - m for manual legals
        - in this mode shift+1..9 will add/remove legals
    - r to start new game on game over, b to go back  
    Mouse
    - click to select cell
    - when game is over click to reset
