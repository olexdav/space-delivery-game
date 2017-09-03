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
    import pygame  # Need this for pygame.image.load()
    import pymunk
    import math  # Need this for math.radians()
    import sys
except ImportError as exc:
    print("(!) Could not load module {}, exiting...".format(exc))
    sys.exit(-1)


class Collidable:
    """
    Class that represents a physical object in the game
    """
    def __init__(self, image_dir, x=0, y=0, angle=0, density=1, body_type='dynamic', shape_type='box'):
        self.sprite = pygame.image.load(image_dir).convert_alpha()  # Surface with the collidable's image
        self.body = None
        self.set_body(x=x, y=y, angle=angle, density=density,
                      body_type=body_type, shape_type=shape_type)  # Physical body
        self.shape = None
        self.set_shape(shape_type)  # Shape of the body

    def set_body(self, x=0, y=0, angle=0, density=1, body_type='dynamic', shape_type='box'):
        """Generates body for the collidable based on its sprite

        Mass and momentum will be calculated based on the body's shape, sprite and density

        Args:
            x: position in world coordinates
            y: position in world coordinates
            angle: angle in degrees
            density: mass per pixel
            body_type: 'dynamic', 'static' or 'kinematic'
            shape_type: 'box' or 'circle'
        """
        if body_type is 'dynamic':  # Calculate mass and moment for different shapes
            mass = 0
            moment = 0
            if shape_type is 'box':
                mass = density * self.sprite.get_width() * self.sprite.get_height()
                moment = self.sprite.get_width() * self.sprite.get_height() ** 3 / 12
            elif shape_type is 'circle':
                radius = min(self.sprite.get_width(), self.sprite.get_height()) / 2
                mass = density * 3.1415 * radius * radius
                moment = 3.1415 * radius ** 4 / 4
            else:
                raise ValueError("(!) Error: creating body of invalid shape")
            self.body = pymunk.Body(mass=mass, moment=moment, body_type=pymunk.Body.DYNAMIC)
            self.place(x, y, angle)
        elif body_type is 'static':
            self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
            self.place(x, y, angle)
        else:
            raise ValueError("(!) Error: creating body of invalid type")

    def set_shape(self, shape_type='box'):
        """Generates shape for the collidable based on its sprite"""
        if shape_type is 'box':
            self.shape = pymunk.Poly.create_box(self.body, self.sprite.get_size(), 0.01)
        elif shape_type is 'circle':
            radius = min(self.sprite.get_width(), self.sprite.get_height()) / 2
            self.shape = pymunk.Circle(self.body, radius)
        else:
            raise ValueError("(!) Error: creating shape of invalid type")

    def get_position(self):
        """Returns this collidable's position in world coordinates"""
        return self.body.position

    def place(self, world_x, world_y, angle):
        """Places body at particular coordinates rotated by an angle(in degrees)"""
        self.body.position = world_x, world_y
        self.body.angle = math.radians(angle)
