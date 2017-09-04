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
    import pymunk  # Need this for Vec2d
    import sys
except ImportError as exc:
    print("(!) Could not load module {}, exiting...".format(exc))
    sys.exit(-1)

class Camera:
    """
    Utility class for a camera that follows the player
    """
    def __init__(self, view_width, view_height, x=0, y=0):
        self.view_width = view_width  # Basically window size
        self.view_height = view_height
        self.x = x  # These are world coordinates for the center of the camera's view
        self.y = y
        self.angle = 0  # Angle of camera rotation
        self.rotate_towards = 0  # Angle that the camera rotates towards
        self.rotation_speed = 90  # Degrees per second
        self.collidable_to_follow = None  # Collidable that the camera is following
        self.player_to_follow = None  # Player that the camera is following

    def world_to_viewport(self, world_coordinates):
        """Converts world coordinates to viewport coordinates"""
        coordinate_x = world_coordinates[0] - self.x
        coordinate_y = world_coordinates[1] - self.y
        vec = pymunk.Vec2d(coordinate_x, coordinate_y)
        vec.rotate_degrees(-self.angle)
        vec.x += self.view_width / 2
        vec.y += self.view_height / 2
        return int(vec.x), int(vec.y)

    def point_at(self, x, y):
        """Points camera at specific coordinates in the world"""
        self.x = x
        self.y = y

    def follow_collidable(self, collidable):
        """Sets the camera to start following a collidable"""
        self.collidable_to_follow = collidable

    def follow_player(self, player):
        """Sets the camera to start following a player"""
        self.player_to_follow = player

    def update(self, time_delta):
        """Updates camera position (rotating, following things)"""
        if self.collidable_to_follow:  # Follow collidable
            self.point_at(*(self.collidable_to_follow.get_position()))
        if self.player_to_follow:  # Follow player
            world_x, world_y, angle = self.player_to_follow.get_data_for_camera()
            self.point_at(world_x, world_y)  # Point at player's position
            if angle:                        # Rotate if needed
                self.rotate_towards = angle
        if self.angle is not self.rotate_towards:  # Rotate with time
            rotation = self.rotation_speed * time_delta
            if self.angle < self.rotate_towards:
                self.angle += rotation
                if self.angle > self.rotate_towards:
                    self.angle = self.rotate_towards
            elif self.angle > self.rotate_towards:
                self.angle -= rotation
                if self.angle < self.rotate_towards:
                    self.angle = self.rotate_towards

    def near_viewport(self, position):
        """Returns true if the position(world coordinates) is close to the viewport and can be rendered"""
        view_x, view_y = self.world_to_viewport(position)
        margin = 600  # Distance in pixels, any object that is further from the viewport will be ignored
        if view_x < -margin or view_y < -margin:
            return False
        elif view_x > self.view_width + margin or view_y > self.view_height + margin:
            return False
        else:
            return True

    def start_turn(self, angle_towards):
        """Starts slowly turning the camera around"""
        self.rotate_towards = angle_towards