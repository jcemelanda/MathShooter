#! /usr/bin/env python
"""
#   Math Shooter.
#   A math scrolling arcade shooter.
#   This code is based in the one written by Tyler Gray & Chad Haley and
#   released under GPL
#
#   Copyleft (C) 2009  Julio Melanda
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
#	The song Stone Fortress use as background music of the game was taken from
#	http://opengameart.org/content/stone-fortress
#
"""

from game import Game

if __name__ == "__main__":
    game = Game()
    game.main_loop()
