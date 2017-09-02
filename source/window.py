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
    from camera import Camera
except ImportError as exc:
    print("(!) Could not load module {}, exiting...".format(exc))
    sys.exit(-1)

class Window():
    """
    Class that handles window creation, resizing and rendering
    """

    def __init__(self, width=800, height=600, caption="untitled", flags=0, icon=None):
        self.resolution = [width, height]
        self.fullscreen = False
        self.screen = pygame.display.set_mode(self.resolution, flags)
        pygame.display.set_caption(caption)
        self.rect = self.screen.get_rect()
        if icon is not None: pygame.display.set_icon(icon)
        self.camera = Camera()

    # Fills window with color
    def fill(self, color):
        self.screen.fill(color)

    # Draws a sprite onto the screen
    def draw(self, sprite, world_coordinates):
        x, y = self.camera.world_to_viewport(world_coordinates) # Convert coordinates to viewport
        x -= sprite.get_width()/2 # Align coordinates
        y -= sprite.get_height()/2 # so the sprite's pivot is centered
        self.screen.blit(sprite, (x,y))

    def update(self):
        #pygame.display.flip()
        pygame.display.update(self.rect)

    @staticmethod
    def get_resolution():
        return pygame.display.get_surface().get_size()

    # Toggles fullscreen without changing resolution
    def toggle_fullscreen(self):
        if self.fullscreen is False:
            self.screen = pygame.display.set_mode(self.resolution, pygame.FULLSCREEN)
            self.fullscreen = True
        elif self.fullscreen:
            self.screen = pygame.display.set_mode(self.resolution)
            self.fullscreen = False