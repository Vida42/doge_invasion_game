#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-24 23:18:03
# @Author  : Amano
# @Version : $Id$

import pygame
from pygame.sprite import Sprite

class Doge(Sprite):
    """A class to represent a single doge in the fleet"""

    def __init__(self, ai_settings, screen):
        """Initialize the doge and set its starting position"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the doge image and set its rect attribute
        self.image = pygame.image.load('images/doge.bmp')
        self.rect = self.image.get_rect()

        # Start each new doge near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the doge's exact position
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if doge is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the doge right or left"""
        self.x += (self.ai_settings.doge_speed_factor * 
            self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        """Draw the doge at its current location"""
        self.screen.blit(self.image, self.rect)