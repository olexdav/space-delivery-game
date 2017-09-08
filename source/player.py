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
    import pymunk
    import sys
    from utils import angle_difference
    from collidable import Collidable
except ImportError as exc:
    print("(!) Could not load module {}, exiting...".format(exc))
    sys.exit(-1)


class Player:
    """
    Class that handles player's car in-game
    """
    def __init__(self):
        # The main collidable for the player's car
        self.car = Collidable(image_dir="../resources/images/player_car.png",
                              x=0,
                              y=0,
                              density=1,
                              body_type='dynamic',
                              shape_type='box')
        self.car.body.damping = 0.9  # Adjust damping for better control
        self.movement_angle = 90  # Angle that the player is moving towards
        self.alignment_spring_pivot = pymunk.Body(body_type=pymunk.Body.STATIC)  # Pivot to control the spring
        self.alignment_spring_pivot.angle = math.radians(self.movement_angle)  # Align spring with the movement angle
        # A spring that aligns the car so it faces forward in the tunnels
        self.alignment_spring = pymunk.DampedRotarySpring(a=self.car.body,
                                                          b=self.alignment_spring_pivot,
                                                          rest_angle=0.0,
                                                          stiffness=150000000.0,
                                                          damping=75000000.0)
        self.level = None  # Reference to the level that the player is in
        self.steered_this_frame = False  # If there was keyboard input in this frame (steering the car)
        self.steering_force = 1500000  # How quickly the car rotates

    # TODO: movement methods should be transferred to a separate Car class so the AI can make use of them

    def accelerate(self):
        """Accelerates the car forward"""
        self.car.body.apply_force_at_local_point(force=(0, -8000000), point=(0, 0))
        # TODO: limit top speed

    def decelerate(self):
        """Decelerates the car"""
        self.car.body.apply_force_at_local_point(force=(0, 8000000), point=(0, 0))
        # TODO: make sure the car's velocity never drops below zero (no backpedaling)

    def steer_right(self):
        """Steers the car to the right"""
        self.rotate_right(self.steering_force)
        self.steered_this_frame = True

    def steer_left(self):
        """Steers the car to the left"""
        self.rotate_left(self.steering_force)
        self.steered_this_frame = True

    def rotate_right(self, force):
        """Rotates the car by applying force"""
        self.car.body.apply_force_at_local_point(force=(force, 0), point=(0, -70))  # Front left thruster
        self.car.body.apply_force_at_local_point(force=(-force, 0), point=(0, 70))  # Back right thruster

    def rotate_left(self, force):
        """Rotates the car by applying force"""
        self.car.body.apply_force_at_local_point(force=(-force, 0), point=(0, -70))  # Front right thruster
        self.car.body.apply_force_at_local_point(force=(force, 0), point=(0, 70))  # Back left thruster

    def turn_right(self):
        """Changes the car's movement direction by 90 degrees to the right"""
        self.change_movement_direction(self.movement_angle + 90)

    def turn_left(self):
        """Changes the car's movement direction by 90 degrees to the left"""
        self.change_movement_direction(self.movement_angle - 90)

    def change_movement_direction(self, angle):
        """Sets the car on course to a particular angle"""
        self.movement_angle = angle   # Set general movement direction
        self.alignment_spring_pivot.angle = math.radians(angle)  # Rotate the alignment spring

    def place_in_world(self, world):
        """Places player at the level's spawn"""
        self.level = world.level  # Save reference to the level
        self.car.place(*(self.level.get_player_spawn()))  # Place car at the spawn
        world.physics.space.add(self.alignment_spring_pivot, self.alignment_spring)  # Add spring
        world.add_collidable(self.car)  # Add the car to the world

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
        car_angle = self.get_car_angle()
        tunnel_orientation = self.determine_tunnel_orientation()
        if tunnel_orientation is "Horizontal":
            if 0 <= car_angle <= 180:
                cam_angle = 90
            else:
                cam_angle = 270
        elif tunnel_orientation is "Vertical":
            if 90 <= car_angle <= 270:
                cam_angle = 180
            else:
                cam_angle = 360
        return world_x, world_y, cam_angle

    def get_car_angle(self):
        """Returns car angle in degrees [0,359]"""
        return int(math.degrees(self.car.body.angle)) % 360