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
    import sys
    from window import Window
    from player import Player
    from world import World
except ImportError as exc:
    print("(!) Could not load module {}, exiting...".format(exc))
    sys.exit(-1)

GAME_VERSION = "v0.1"

class Game:
    """
    Class that describes the general game logic
    """

    def __init__(self, fps=60):
        self.fps = fps
        self.clock = pygame.time.Clock() # Clock to keep track of time
        self.window = None
        self.player = None

    # Initializes everything and starts main game loop
    def run(self):
        self.init_pygame()
        self.create_window()
        self.show_loading_screen()
        self.init()
        self.main_loop()

    # Creates a pygame window
    def create_window(self):
        self.window = Window(800, 600, "space-delivery-game", 0)

    # Displays a splash screen
    def show_loading_screen(self):
        pass

    # Initializes things that are global in the scope of the game
    def init(self):
        self.player = Player() # Load player
        self.world = World() # Create world

    # Initializes pygame
    def init_pygame(self):
        check_errors = pygame.init()
        if check_errors[1] > 0:
            print("(!) Had {0} errors initializing PyGame, exiting...".format(check_errors[1]))
            sys.exit(-1)
        else:
            print("(+) PyGame successfully initialized!")

    # Runs the game frame by frame
    def main_loop(self):
        while not pygame.event.peek(pygame.QUIT):
            pass # Update current state
            self.window.fill((130, 200, 100)) # Draw background
            self.window.draw(self.player.car.sprite, (0,0)) # Draw player
            self.window.update() # Update the window
            pass # Update physics
            self.clock.tick(self.fps)  # Limit fps
            # Show current fps in the window title
            pygame.display.set_caption("space-delivery-game {ver} fps: {fps}".format(ver=GAME_VERSION,
                                                                                    fps=str(int(self.clock.get_fps()))))
