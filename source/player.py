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

    # TODO: movement methods should be transferred to a separate Car class so the AI can make use of them

    def accelerate(self):
        """Accelerates the car forward"""
        self.car.body.apply_impulse_at_local_point(impulse=(0, -100000), point=(0, 0))

    def decelerate(self):
        """Decelerates the car"""
        self.car.body.apply_impulse_at_local_point(impulse=(0, 100000), point=(0, 0))
        # TODO: make sure the car's velocity never drops below zero (no backpedaling)

    def steer_right(self):
        """Steers the car to the right"""
        self.car.body.apply_impulse_at_local_point(impulse=(10000, 0), point=(0, -70)) # Front left thruster
        self.car.body.apply_impulse_at_local_point(impulse=(-10000, 0), point=(0, 70)) # Back right thruster

    def steer_left(self):
        """Steers the car to the left"""
        self.car.body.apply_impulse_at_local_point(impulse=(-10000, 0), point=(0, -70))  # Front right thruster
        self.car.body.apply_impulse_at_local_point(impulse=(10000, 0), point=(0, 70))    # Back left thruster

