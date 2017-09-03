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


class Camera:
    """
    Utility class for a camera that follows the player
    """
    def __init__(self, view_width, view_height, x=0, y=0):
        self.view_width = view_width  # Basically window size
        self.view_height = view_height
        self.x = x  # These are world coordinates for the center of the camera's view
        self.y = y
        self.following = None  # Collidable that the camera is following

    def world_to_viewport(self, world_coordinates):
        """Converts world coordinates to viewport coordinates"""
        coordinate_x = world_coordinates[0] - self.x + self.view_width / 2
        coordinate_y = world_coordinates[1] - self.y + self.view_height / 2
        return int(coordinate_x), int(coordinate_y)

    def point_at(self, x, y):
        """Points camera at specific coordinates in the world"""
        self.x = x
        self.y = y

    def follow(self, collidable):
        """Sets the camera to start following a collidable"""
        self.following = collidable

    def unfollow(self):
        """Orders the camera to stop following a collidable"""
        self.following = None

    def update(self):
        """Updates camera position (following a collidable)"""
        if self.following:
            self.point_at(*(self.following.get_position()))