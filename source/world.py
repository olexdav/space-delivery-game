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
    import sys
    from physics import Physics
    from collidable import Collidable
    from level import Level
except ImportError as exc:
    print("(!) Could not load module {}, exiting...".format(exc))
    sys.exit(-1)


class World:
    """
    Class that includes all objects in a level and handles interaction between them
    """
    def __init__(self):
        self.physics = Physics()  # Add a physics handler
        self.level = Level()      # Add a level layout
        self.level.generate_test_level()  # DEBUG: create a test level
        self.walls = []

    def update(self, fps):
        """Updates the whole world by one frame"""
        self.physics.update(fps)  # Update physics

    def render(self, window):
        """Renders all world objects to the window"""
        for wall in self.walls:
            window.draw_collidable(wall)

    def add_collidable(self, collidable):
        """Adds a collidable to the physical simulation"""
        self.physics.add_collidable(collidable)

    def build_from_level(self):
        """Builds the world's physical objects from level layout"""
        wall_positions = self.level.export_walls()
        for wall_position in wall_positions:
            if wall_position[2] is "Vertical":
                angle = 0
            elif wall_position[2] is "Horizontal":
                angle = 90
            wall = Collidable(image_dir="../resources/images/side_wall.png",
                              x=wall_position[0],
                              y=wall_position[1],
                              angle=angle,
                              body_type='static',
                              shape_type='box')
            self.walls.append(wall)            # Save wall
            self.add_collidable(wall)  # Add wall to physical simulation
