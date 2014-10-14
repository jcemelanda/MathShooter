# -*- coding:utf8 -*-
from unittest.case import TestCase
import pygame
from MathShooter import Game

__author__ = 'julio'

class GameTest(TestCase):
    game = None

    def test_game_start(self):
        self.game = Game()
        assert self.game

    def test_start_menu(self):
        self.game = Game()
        self.game.main_menu()
        pygame.quit()

