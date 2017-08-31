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
except ImportError as exc:
    print("Could not load module {}.".format(exc))

class Window():
    def __init__(self, width=800, height=600, caption="untitled", flags=0, icon=None):
        self.resolution = [width, height]
        self.fullscreen = False
        self.screen = pygame.display.set_mode(self.resolution, flags)
        pygame.display.set_caption(caption)
        self.rect = self.screen.get_rect()
        if icon is not None: pygame.display.set_icon(icon)
    def update(self):
        #pygame.display.flip()
        pygame.display.update(self.rect)
    def getResolution(self):
        return pygame.display.get_surface().get_size()
    def toggleFullscreen(self):
        if self.fullscreen is False:
            self.screen = pygame.display.set_mode(self.resolution, pygame.FULLSCREEN)
            self.fullscreen = True
        elif self.fullscreen:
            self.screen = pygame.display.set_mode(self.resolution)
            self.fullscreen = False