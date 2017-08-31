"""
    This file is part of space-delivery-game.

    space-delivery-game is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    space-delivery-game is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with space-delivery-game.  If not, see <http://www.gnu.org/licenses/>.


    Copyright(C) 2017 Oleksii Davydenko
"""

try:
    import pygame
    from window import Window
except ImportError as exc:
    print("Could not load module {}.".format(exc))

GAME_VERSION = "v0.1"

class Game:
    """
    Class that describes the general game logic
    """

    def __init__(self, fps=60):
        self.fps = fps
        self.clock = pygame.time.Clock() # a clock to keep track of time

    # Initializes everything and starts main game loop
    def run(self):
        self.createWindow()
        self.showLoadingScreen()
        self.init()
        self.mainLoop()

    # Creates a pygame window
    def createWindow(self):
        self.window = Window(800, 600, "space-delivery-game", 0)

    # Displays a splash screen
    def showLoadingScreen(self):
        pass

    # Initializes things that are global in the scope of the game
    def init(self):
        pass

    # Runs the game frame by frame
    def mainLoop(self):
        while not pygame.event.peek(pygame.QUIT):
            self.clock.tick(self.fps)  # Limit the fps
            pass # Update current state
            pass # Update the window
            # Show current fps in the window title
            pygame.display.set_caption("space-delivery-game {ver} fps: {fps}".format(ver=GAME_VERSION,
                                                                                    fps=str(int(self.clock.get_fps()))))
