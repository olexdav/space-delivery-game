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


class Level:
    """
    Class for generating a level layout, including walls, mobs and obstacles

    Coordinates work the same way as in pymunk
    X: left to right
    Y: top to bottom
    """
    def __init__(self):
        self.junctions = []          # All junctions in the level
        self.tunnels = []            # All tunnels in the level
        self.entry_point = None      # The point where player enters the level
        self.entry_direction = None  # Direction to the first tunnel that the player goes through
        # TODO: this should scale with screen resolution
        # This should always be equal to (wall sprite height - wall sprite width)
        self.grid_size = 920        # Size of each cell on the map grid in pixels (50px is approximately 1 meter)

    def generate_test_level(self):
        """Generates a basic level"""
        # Looks     #---#     Legend:
        # like      |   |   # - junctions
        # this: @->-#---#   | - tunnels
        #       |   |   |   @ - entry point
        #       #---#---#   > - entry tunnel
        # TODO: write unit tests for the Level class
        # TODO: also unit tests for Collidable class
        level_scale = 4  # Length of the tunnels (starts at 2)
        self.junctions.append(Junction(level_scale, 0))
        self.junctions.append(Junction(level_scale * 2, 0))
        self.junctions.append(Junction(0, level_scale))
        self.junctions.append(Junction(level_scale, level_scale))
        self.junctions.append(Junction(level_scale * 2, level_scale))
        self.junctions.append(Junction(0, level_scale * 2))
        self.junctions.append(Junction(level_scale, level_scale * 2))
        self.junctions.append(Junction(level_scale * 2, level_scale * 2))
        for x in range(10):
            self.tunnels.append(Tunnel())
        self.join_existing(0, 0, 1)
        self.join_existing(2, 1, 3)
        self.join_existing(3, 2, 4)
        self.join_existing(5, 3, 6)
        self.join_existing(6, 4, 7)
        self.join_existing(2, 5, 5)
        self.join_existing(3, 6, 6)
        self.join_existing(4, 7, 7)
        self.join_existing(0, 8, 3)
        self.join_existing(1, 9, 4)
        self.entry_point = self.junctions[2]
        self.entry_direction = 'right'

    @staticmethod
    def join(junction_from, tunnel, junction_to):
        """Joins two junctions with a tunnel

        Args:
            junction_from: A Junction that will become the beginning of the tunnel
            tunnel: A Tunnel that will join the junctions
            junction_to: A Junction that will become the end of the tunnel

        Raises:
            RuntimeError: If junctions are not properly aligned (on one horizontal or vertical line)
        """
        if not isinstance(junction_from, Junction)\
                or not isinstance(junction_to, Junction)\
                or not isinstance(tunnel, Tunnel):
            raise AttributeError("(!) Error: Level.join() uses Junction and Tunnel arguments")
        # Set tunnel orientation
        if junction_from.y == junction_to.y:    # Horizontal
            tunnel.orientation = "Horizontal"
        elif junction_from.x == junction_to.x:  # Vertical
            tunnel.orientation = "Vertical"
        else:
            raise RuntimeError("(!) Error: trying to join junctions that are not properly aligned")
        # Break walls to accomodate the tunnel
        if tunnel.orientation is "Horizontal":
            if junction_from.x < junction_to.x:
                junction_from.walls['right'] = False
                junction_to.walls['left'] = False
            elif junction_from.x > junction_to.x:
                junction_from.walls['left'] = False
                junction_to.walls['right'] = False
            else:
                raise RuntimeError("(!) Error: trying to join two junctions with equal coordinates")
        elif tunnel.orientation is "Vertical":
            if junction_from.y < junction_to.y:
                junction_from.walls['down'] = False
                junction_to.walls['up'] = False
            elif junction_from.y > junction_to.y:
                junction_from.walls['up'] = False
                junction_to.walls['down'] = False
            else:
                raise RuntimeError("(!) Error: trying to join two junctions with equal coordinates")
        # Finalize
        tunnel.junctions[0] = junction_from  # Add junctions to tunnel
        tunnel.junctions[1] = junction_to
        junction_from.tunnels.append(tunnel)  # Add tunnel to junctions
        junction_to.tunnels.append(tunnel)

    def join_existing(self, junction_from, tunnel, junction_to):
        """Joins two junctions with a tunnel

        The difference from join() is that the joined objects must already exist in
        self.junctions or self.tunnels

        Args:
            junction_from: An integer index of a junction from self.junctions
            tunnel: An integer index of a tunnel from self.tunnels
            junction_to: An integer index of a junction from self.junctions

        Raises:
            TypeError: If any of the arguments is not integer
            IndexError: If tunnel or junction indices are out of range
            RuntimeError: If junctions are not properly aligned (on one horizontal or vertical line)
        """
        if not isinstance(junction_from, int) or not isinstance(junction_to, int) or not isinstance(tunnel, int):
            raise TypeError("(!) Error: Level.join_existing() uses integer arguments")
        j_from = self.junctions[junction_from]
        j_to = self.junctions[junction_to]
        t_through = self.tunnels[tunnel]
        Level.join(j_from, t_through, j_to)

    def export_walls(self):
        """Exports all walls in the level

        Wall positions are exported to be added to the World and the physical simulation.
        Wall orientation is either "Horizontal" or "Vertical"

        Returns:
            A list wall_positions where each element is (world_x, world_y, orientation)
        """
        wall_positions = []
        for junction in self.junctions:  # Add walls of every junction
            wall_positions.extend(self.export_junction_walls(junction))
        for tunnel in self.tunnels:  # Add walls of every tunnel
            wall_positions.extend(self.export_tunnel_walls(tunnel))
        return wall_positions

    def export_tunnel_walls(self, tunnel):
        """Exports walls of a particular tunnel

        Returns:
            A list wall_positions where each element is (world_x, world_y, orientation)

        Raises:
            TypeError: If tunnel is not of type Tunnel
        """
        if not isinstance(tunnel, Tunnel):
            raise TypeError("(!) Error: trying to export walls of a non-tunnel object")
        wall_positions = []
        if tunnel.orientation is "Horizontal":
            left = tunnel.get_left_bound()  # Get tunnel bounds
            right = tunnel.get_right_bound()
            y = tunnel.get_top_bound()
            for x in range(left, right+1):
                wall_x, wall_y = self.wall_coordinates(x, y, 'up')  # Make two walls for each cell
                wall_positions.append((wall_x, wall_y, "Horizontal"))
                wall_x, wall_y = self.wall_coordinates(x, y, 'down')
                wall_positions.append((wall_x, wall_y, "Horizontal"))
        elif tunnel.orientation is "Vertical":
            top = tunnel.get_top_bound()  # Get tunnel bounds
            bottom = tunnel.get_bottom_bound()
            x = tunnel.get_left_bound()
            for y in range(top, bottom+1):
                wall_x, wall_y = self.wall_coordinates(x, y, 'left')  # Make two walls for each cell
                wall_positions.append((wall_x, wall_y, "Vertical"))
                wall_x, wall_y = self.wall_coordinates(x, y, 'right')
                wall_positions.append((wall_x, wall_y, "Vertical"))
            pass
        return wall_positions


    def export_junction_walls(self, junction):
        """Exports walls of a particular junction

        Returns:
            A list wall_positions where each element is (world_x, world_y, orientation)

        Raises:
            TypeError: If junction is not of type Junction
        """
        if not isinstance(junction, Junction):
            raise TypeError("(!) Error: trying to export walls of a non-junction object")
        wall_positions = []
        for direction in junction.walls.keys():  # For all four directions
            if junction.walls[direction]:        # Add walls if they exist
                wall_x, wall_y = self.wall_coordinates(junction.x, junction.y, direction)
                if direction is 'right' or direction is 'left':
                    orientation = "Vertical"
                else:
                    orientation = "Horizontal"
                wall_positions.append((wall_x, wall_y, orientation))
        return wall_positions

    def wall_coordinates(self, x, y, type):
        """Returns world coordinates of a wall at level coordinates (x,y)

        Args:
            x: coordinate on level grid
            y: coordinate on level grid
            type: type of the wall ('left', 'right', 'up', 'down')
        Returns:
            world_x, world_y: coordinates in world space
        Raises:
            ValueError: If the wall type is invalid
        """
        world_x = x * self.grid_size
        world_y = y * self.grid_size
        if type is 'right':
            world_x += self.grid_size
            world_y += self.grid_size / 2
        elif type is 'left':
            world_y += self.grid_size / 2
        elif type is 'up':
            world_x += self.grid_size / 2
        elif type is 'down':
            world_x += self.grid_size / 2
            world_y += self.grid_size
        else:
            raise ValueError("(!) Error: wall type is invalid")
        return world_x, world_y

    def get_player_spawn(self):
        """Returns world coordinates and angle of the player's spawn

        Returns:
            world_x, world_y, angle
        """
        world_x = self.grid_size * self.entry_point.x + self.grid_size / 2
        world_y = self.grid_size * self.entry_point.y + self.grid_size / 2
        angle = None
        if self.entry_direction is 'up':
            angle = 0
        elif self.entry_direction is 'right':
            angle = 90
        elif self.entry_direction is 'down':
            angle = 180
        elif self.entry_direction is 'left':
            angle = 270
        return world_x, world_y, angle

    def world_to_grid(self, world_x, world_y):
        """Converts world coordinates to level grid coordinates"""
        return int(world_x / self.grid_size), int(world_y / self.grid_size)

    def get_tunnel_orientation(self, world_x, world_y):
        """Determines the orientation of the tunnel at world coordinates"""
        grid_x, grid_y = self.world_to_grid(world_x, world_y)
        orientation = None
        for tunnel in self.tunnels:
            if tunnel.includes(grid_x, grid_y):
                orientation = tunnel.orientation
                break
        return orientation


class Tunnel:
    """
    A straight tunnel between two junctions
    """
    def __init__(self):
        self.junctions = [None, None]  # Two adjacent junctions
        self.orientation = None        # If the tunnel is horizontal or vertical

    def get_left_bound(self):
        """Returns the left bound of the tunnel in level coordinates"""
        # Bounds DO NOT include junctions
        if self.orientation is "Vertical":
            return self.junctions[0].x
        elif self.orientation is "Horizontal":
            return min(self.junctions[0].x, self.junctions[1].x)+1

    def get_right_bound(self):
        """Returns the right bound of the tunnel in level coordinates"""
        if self.orientation is "Vertical":
            return self.junctions[0].x
        elif self.orientation is "Horizontal":
            return max(self.junctions[0].x, self.junctions[1].x)-1

    def get_top_bound(self):
        """Returns the top bound of the tunnel in level coordinates"""
        if self.orientation is "Horizontal":
            return self.junctions[0].y
        elif self.orientation is "Vertical":
            return min(self.junctions[0].y, self.junctions[1].y)+1

    def get_bottom_bound(self):
        """Returns the bottom bound of the tunnel in level coordinates"""
        if self.orientation is "Horizontal":
            return self.junctions[0].y
        elif self.orientation is "Vertical":
            return max(self.junctions[0].y, self.junctions[1].y)-1

    def includes(self, grid_x, grid_y):
        """Checks if the tunnel includes a particular grid cell"""
        return self.get_left_bound() <= grid_x <= self.get_right_bound() \
                and self.get_top_bound() <= grid_y <= self.get_bottom_bound()


class Junction:
    """
    A place where two or more tunnels meet
    """
    def __init__(self, x=0, y=0):
        self.x = x  # Location on the level grid
        self.y = y
        self.tunnels = []  # Two to four adjacent tunnels
        self.walls = { 'up': True, 'down': True, 'left': True, 'right': True }  # Walls forming the junction
