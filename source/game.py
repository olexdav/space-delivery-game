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
    import math  # Need this for math.degrees()
    import sys
    from window import Window
    from player import Player
    from world import World
    from inputhandler import InputHandler
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
        self.clock = pygame.time.Clock()  # Clock to keep track of time
        self.window = None
        self.world = None
        self.player = None
        self.input_handler = InputHandler()

    def run(self):
        """Initializes everything and starts main game loop"""
        self.init_pygame()          # Initialize engine
        self.create_window()        # Create app window
        self.show_loading_screen()  # Show splash screen
        self.init()                 # Load game
        self.main_loop()            # The grand loop
        pygame.quit()               # Exit game
        sys.exit()

    def create_window(self):
        """Creates a pygame window"""
        self.window = Window(1920, 1080, "space-delivery-game", 0)
        #self.window.toggle_fullscreen()

    def show_loading_screen(self):
        """Displays a splash screen"""
        pass

    def init(self):
        """Initializes things that are global in the scope of the gam"""
        self.world = World()           # Create world
        self.world.build_from_level()  # Add level to the world
        self.spawn_player()            # Add player to the world

    def init_pygame(self):
        """Initializes pygame"""
        check_errors = pygame.init()
        if check_errors[1] > 0:
            print("(!) Had {0} errors initializing PyGame, exiting...".format(check_errors[1]))
            sys.exit(-1)
        else:
            print("(+) PyGame successfully initialized!")

    def main_loop(self):
        """Runs the game frame by frame"""
        while not pygame.event.peek(pygame.QUIT):
            milliseconds = self.clock.tick(self.fps)  # Limit fps
            time_delta = milliseconds / 1000.0  # Seconds passed since last frame
            pass  # Update current state
            self.handle_input()  # Handle input
            self.world.update(time_delta)  # Update world (physics, etc.)
            self.player.update(time_delta)  # Update the player
            self.window.camera.update(time_delta)  # Move the camera
            self.render() # Draw everything
            # Show current fps in the window title
            pygame.display.set_caption("space-delivery-game {ver} fps: {fps}".format(ver=GAME_VERSION,
                                                                                    fps=str(int(self.clock.get_fps()))))

    def handle_input(self):
        """Handles all input"""
        self.input_handler.update()  # Update input handler
        # Control player
        if self.input_handler.keypress[ord('w')]:    # Accelerate
            self.player.accelerate()
        elif self.input_handler.keypress[ord('s')]:  # Decelerate
            self.player.decelerate()
        if self.input_handler.keypress[ord('a')]:    # Steer left
            self.player.steer_left()
        elif self.input_handler.keypress[ord('d')]:  # Steer right
            self.player.steer_right()

    def render(self):
        """Renders everything"""
        self.window.fill((130, 200, 100))  # Draw background
        self.world.render(self.window)  # Draw the world
        self.window.draw_collidable(self.player.car)  # Draw player
        self.window.update()  # Update the window

    def spawn_player(self):
        """Creates a player and adds him to the world"""
        self.player = Player()  # Load player
        self.player.place_in_level(self.world.level)  # Place player in the level
        self.world.add_collidable(self.player.car)  # Add player to the world
        self.window.camera.follow_player(self.player)  # Follow player with the camera
        self.window.camera.start_turn(math.degrees(self.player.car.body.angle))  # Align camera with the player
        #self.window.camera.angle = math.degrees(self.player.car.body.angle)  # Align camera with the player
