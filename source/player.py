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
        self.car = Collidable(image_dir="../resources/images/player_car.png",
                              x=0,
                              y=0,
                              density=1,
                              body_type='dynamic',
                              shape_type='box')
        self.level = None  # Level that the player is in
        # TEMP
        self.movement_angle = 90  # Angle that the player is moving towards
        self.steered_this_frame = False  # If there was keyboard input in this frame (steering the car)
        self.steering_force = 800000  # How quickly the car rotates
        self.alignment_time = 1  # Amount of seconds it takes to automatically align the car
        self.alignment_time_left = 0  # Monitor how much time is left to align the car

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
        self.turn_right(self.steering_force)
        self.steered_this_frame = True

    def steer_left(self):
        """Steers the car to the left"""
        self.turn_left(self.steering_force)
        self.steered_this_frame = True

    def turn_right(self, force):
        """Turns the car by applying force"""
        self.car.body.apply_force_at_local_point(force=(force, 0), point=(0, -70))  # Front left thruster
        self.car.body.apply_force_at_local_point(force=(-force, 0), point=(0, 70))  # Back right thruster

    def turn_left(self, force):
        """Turns the car by applying force"""
        self.car.body.apply_force_at_local_point(force=(-force, 0), point=(0, -70))  # Front right thruster
        self.car.body.apply_force_at_local_point(force=(force, 0), point=(0, 70))  # Back left thruster

    # TEMP
    def apply_impulse(self, impulse):
        """TEMP"""
        self.car.body.apply_impulse_at_local_point(impulse=(impulse, 0), point=(0, -70))  # Front left thruster
        self.car.body.apply_impulse_at_local_point(impulse=(-impulse, 0), point=(0, 70))  # Back right thruster

    def update(self, time_delta):
        """Updates things related to movement"""
        if self.alignment_time_left > 0:  # Align the car
            #time_used = min(time_delta, self.alignment_time_left)  # Don't take too much time
            time_used = 1/60.0 # TEMP
            ang_target = math.radians(self.movement_angle)  # Target angle
            ang_curr = math.radians(self.get_car_angle())   # Current angle
            ang_vel = self.car.body.angular_velocity        # Angular velocity
            I = self.car.body.moment                        # Moment of inertia
            r = 70                                          # Distance to point of application of force
            t = self.alignment_time_left                    # Time left to align the car
            force = (ang_target - ang_curr - ang_vel * t) * 2 * I / r / t ** 2  # Calculate force
            #force = ang_vel * 2 * I / r / t  # Calculate force
            impulse = force * time_used   # Apply instant impulse
            if math.fabs(ang_target - ang_curr) < 1e-9: # AAARRGH
                impulse = 0
            self.apply_impulse(impulse / 2)  # Split impulse between two points
            self.alignment_time_left -= time_used  # Tick the clock
            # DEBUG
            print("Aligning: {}s left".format(self.alignment_time_left))
            print("ang_target:{} ang_curr:{} ang_vel:{} t:{} force:{}".format(ang_target, ang_curr, ang_vel, t, force))
        if self.steered_this_frame:  # Initiate alignment after steering
            self.alignment_time_left = self.alignment_time
            self.steered_this_frame = False  # Drop the input flag
        """
        if not self.steered_this_frame: # Unless the car was steered
            # Align car
            car_angle = self.get_car_angle()
            
            angle_diff = angle_difference(car_angle, self.movement_angle)  # Calculate difference with movement angle
            force = abs(angle_diff) / 180 * self.steering_force  # Apply a proper amount of force to align the car
            if angle_diff > 0:
                self.turn_right(force)
            elif angle_diff < 0:
                self.turn_left(force)
            
        self.steered_this_frame = False  # Drop the input flag
        """

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