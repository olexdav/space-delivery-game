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
    import pygame
    import pymunk # TEMP
    import sys
except ImportError as exc:
    print("(!) Could not load module {}, exiting...".format(exc))
    sys.exit(-1)

class Collidable:
    """
    Class that represents a physical object in the game
    """

    def __init__(self, image_dir, x=0, y=0, density=1, body_type='dynamic', shape_type='box'):
        self.x = x
        self.y = y
        self.sprite = pygame.image.load(image_dir).convert_alpha()
        self.body = None
        self.set_body(x, y, density, body_type, shape_type)
        self.shape = None
        self.set_shape(shape_type)

    # Generates body for the collidable based on its sprite
    def set_body(self, x=0, y=0, density=1, body_type='dynamic', shape_type='box'):
        if body_type is 'dynamic': # Calculate mass and moment for different shapes
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
                raise AttributeError("(!) Error: creating body of invalid shape")
            self.body = pymunk.Body(mass, moment, pymunk.Body.DYNAMIC)
            self.body.position = x, y
        elif body_type is 'static':
            self.body = pymunk.Body(pymunk.Body.STATIC)
            self.body.position = x, y
        else:
            raise AttributeError("(!) Error: creating body of invalid type")

    # Generates shape for the collidable based on its sprite
    def set_shape(self, shape_type='box'):
        if shape_type is 'box':
            self.shape = pymunk.Poly.create_box(self.body, self.sprite.get_size(), 0.01)
        elif shape_type is 'circle':
            radius = min(self.sprite.get_width(), self.sprite.get_height()) / 2
            self.shape = pymunk.Circle(self.body, radius)
        else:
            raise AttributeError("(!) Error: creating shape of invalid type")
