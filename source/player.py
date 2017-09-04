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
    import math  # Need this for math.degrees()
    import sys
    from collidable import Collidable
except ImportError as exc:
    print("(!) Could not load module {}, exiting...".format(exc))
    sys.exit(-1)


class Player:
    """
    Class that handles player's car in-game
    """
    def __init__(self):
        self.car = Collidable(image_dir="../resources/images/player_car.png",
                              x=0,
                              y=0,
                              density=1,
                              body_type='dynamic',
                              shape_type='box')
        self.level = None  # Level that the player is in

    # TODO: movement methods should be transferred to a separate Car class so the AI can make use of them

    def accelerate(self):
        """Accelerates the car forward"""
        self.car.body.apply_force_at_local_point(force=(0, -5000000), point=(0, 0))

    def decelerate(self):
        """Decelerates the car"""
        self.car.body.apply_force_at_local_point(force=(0, 5000000), point=(0, 0))
        # TODO: make sure the car's velocity never drops below zero (no backpedaling)

    def steer_right(self):
        """Steers the car to the right"""
        self.car.body.apply_force_at_local_point(force=(500000, 0), point=(0, -70)) # Front left thruster
        self.car.body.apply_force_at_local_point(force=(-500000, 0), point=(0, 70)) # Back right thruster

    def steer_left(self):
        """Steers the car to the left"""
        self.car.body.apply_force_at_local_point(force=(-500000, 0), point=(0, -70))  # Front right thruster
        self.car.body.apply_force_at_local_point(force=(500000, 0), point=(0, 70))    # Back left thruster

    def place_in_level(self, level):
        """Places player at the level's spawn"""
        self.level = level  # Save reference to the level
        self.car.place(*(self.level.get_player_spawn()))  # Place player at the spawn

    def determine_tunnel_orientation(self):
        """Determines the orientation of the tunnel the car is currently in

        Returns:
            "Horizontal", "Vertical" or None
        """
        return self.level.get_tunnel_orientation(*(self.car.get_position()))

    def get_data_for_camera(self):
        """Returns coordinates for the camera to follow

        Returns:
            world_x, world_y, cam_angle: cam_angle can be None (no camera rotation required)
        """
        world_x = self.car.get_position().x  # TEMP
        world_y = self.car.get_position().y
        cam_angle = None
        print(math.degrees(self.car.body.angle))
        # TODO: write camera angle logic
        #tunnel_orientation = self.determine_tunnel_orientation()
        #if tunnel_orientation is "Horizontal"
        return world_x, world_y, cam_angle
