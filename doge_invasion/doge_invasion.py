#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-23 22:59:23
# @Author  : Amano
# @Version : $Id$


import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    # Initialize game and create a screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Doge Invasion")

    # Make the Play button.
    play_button = Button(ai_settings, screen, "PLAY")

    # Make a ship, a group of bullets, and a group of aliens
    ship = Ship(ai_settings, screen)
    bullets = Group()
    doges = Group()

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, doges)

    # Set the background color
    # bg_color = (ai_settings.bg_color)

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Start the main loop for the game
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, doges, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, doges, bullets)
            # gf.update_doges(ai_settings, stats, screen, ship, doges, bullets)
            gf.update_doges(ai_settings, screen, stats, sb, ship, doges, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, doges, bullets, play_button)






run_game()