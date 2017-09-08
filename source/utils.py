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


def angle_difference(angle1, angle2):
    """Calculates difference between two angles, eliminating wrapping issues

    Args:
        angle1: degrees
        angle2: degrees

    Returns:
        difference: [-180,180]
    """
    angle1 = int(angle1) % 360  # Normalize angles
    angle2 = int(angle2) % 360
    difference = angle2-angle1
    if difference < -180:  # Wrap
        difference += 360
    if difference > 180:
        difference -= 360
    return difference


def test():
    """TODO: expand this into actual unit tests"""
    print(angle_difference(240, 350))  # 110
    print(angle_difference(350, 240))  # -110
    print(angle_difference(40, 350))  # -50
    print(angle_difference(350, 40))  # 50