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
except ImportError as exc:
    print("(!) Could not load module {}, exiting...".format(exc))
    sys.exit(-1)


class InputHandler:
    """
    Class that builds on top of pygame to provide advanced input processing
    """
    def __init__(self):
        self.keys = range(ord('a'), ord('z')+1)  # Keys that are being monitored by handler
        values = [False] * len(self.keys)        # Values are true when keys are pressed (between key down and key up)
        self.keypress = dict(zip(self.keys, values))  # { ord('a'): False, ord('b'): False, ... }

    def update(self):
        for event in pygame.event.get():
            if event.type is pygame.KEYDOWN:
                for key in self.keys:
                    if (event.key == key):
                        self.keypress[key] = True
            elif event.type is pygame.KEYUP:
                for key in self.keys:
                    if (event.key == key):
                        self.keypress[key] = False