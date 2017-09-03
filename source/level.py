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
        self.junctions = []       # All junctions in the level
        self.tunnels = []         # All tunnels in the level
        self.entry_point = None   # The point where player enters the level
        self.entry_tunnel = None  # The tunnel that the player first goes through
        # TODO: this should scale with screen resolution
        self.grid_size = 1000     # Size of each cell on the map grid in pixels (50px is approximately 1 meter)

    def generate_test_level(self):
        # Looks     #---#
        # like      |   |
        # this: #---#---#
        #       |   |   |
        #       #---#---#
        # TODO: write unit tests for the Level class
        # TODO: also unit tests for Collidable class
        self.junctions.append(Junction(2, 0))
        self.junctions.append(Junction(4, 0))
        self.junctions.append(Junction(0, 2))
        self.junctions.append(Junction(2, 2))
        self.junctions.append(Junction(4, 2))
        self.junctions.append(Junction(0, 4))
        self.junctions.append(Junction(2, 4))
        self.junctions.append(Junction(4, 4))
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

    @staticmethod
    def join(junction_from, tunnel, junction_to):
        """Joins two junctions with a tunnel

        Args:
            junction_from: A Junction that will become the beginning of the tunnel
            tunnel: A Tunnel that will join the junctions
            junction_to: A Junction that will become the end of the tunnel

        Returns:
            None

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

        Returns:
            None

        Raises:
            AttributeError: If any of the arguments is not integer
            IndexError: If tunnel or junction indices are out of range
            RuntimeError: If junctions are not properly aligned (on one horizontal or vertical line)
        """
        if not isinstance(junction_from, int) or not isinstance(junction_to, int) or not isinstance(tunnel, int):
            raise AttributeError("(!) Error: Level.join_existing() uses integer arguments")
        j_from = self.junctions[junction_from]
        j_to = self.junctions[junction_to]
        t_through = self.tunnels[tunnel]
        Level.join(j_from, t_through, j_to)


class Tunnel:
    """
    A straight tunnel between two junctions
    """
    def __init__(self):
        self.junctions = [None, None]  # Two adjacent junctions
        self.orientation = None        # If the tunnel is horizontal or vertical


class Junction:
    """
    A place where two or more tunnels meet
    """
    def __init__(self, x=0, y=0):
        self.x = x  # Location on the level grid
        self.y = y
        self.tunnels = []  # Two to four adjacent tunnels
        self.walls = { 'up': True, 'down': True, 'left': True, 'right': True }  # Walls forming the junction