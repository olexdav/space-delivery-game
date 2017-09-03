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
    import pymunk
    import sys
except ImportError as exc:
    print("(!) Could not load module {}, exiting...".format(exc))
    sys.exit(-1)


class Physics:
    """
    A handler for all physics in the game
    """
    def __init__(self):
        self.space = pymunk.Space()  # Create a Space which contains the simulation
        self.space.gravity = 0, 0    # Set its gravity

    def update(self, fps):
        """Updates the entire simulation"""
        dt = 1.0 / fps / 2.0
        for x in range(2):
            self.space.step(dt)  # make two updates per frame for better stability

    def add_collidable(self, collidable):
        """Adds a collidable to the physical simulation"""
        self.space.add(collidable.body, collidable.shape)
