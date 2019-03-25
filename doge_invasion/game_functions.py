#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-24 01:08:28
# @Author  : Amano
# @Version : $Id$

import sys
from time import sleep
import pygame
from bullet import Bullet
from doge import Doge

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to keypresses"""
    if event.key == pygame.K_RIGHT:
        # Move the ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # Move the ship to the left
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    """Respond to key releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, doges, bullets):
    """Respond to keypresses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # react to quit game
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                doges,bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            # react to key presses
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            # react to key releases
            check_keyup_events(event, ship)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, doges,
    bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Reset the game statistics
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        doges.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, doges)
        ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, doges, bullets, play_button):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    doges.draw(screen)

    # Redraw all bullets behind ship and doges
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Draw the score information.
    sb.show_score()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible
    pygame.display.flip()

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet"""
    # Create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def update_bullets(ai_settings, screen, stats, sb, ship, doges, bullets):
    """Update position of bullets and get rid of old bullets"""
    # Update bullet positions
    bullets.update()

    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, doges, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, doges, bullets):
    """Respond to bullet-doge collisions."""
    # Remove any bullets and doges that have collided.
    collisions = pygame.sprite.groupcollide(bullets, doges, True, True)

    if collisions:
        for doges in collisions.values():
            stats.score += ai_settings.doge_points * len(doges)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(doges) == 0:
        # Destroy existing bullets, speed up game, and create new fleet.
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, doges)

def get_number_doges_x(ai_settings, doge_width):
    """Determine the number of doges that fit in a row"""
    available_space_x = ai_settings.screen_width - (2 * doge_width)
    number_doges_x = available_space_x // (2 * doge_width)
    return number_doges_x

def get_number_rows(ai_settings, ship_height, doge_height):
    """Determine the number of rows of doges that fit on the screen"""
    available_space_y = (ai_settings.screen_height - 
        (3 * doge_height) - ship_height)
    number_rows = available_space_y // (2 * doge_height)
    return number_rows

def create_doge(ai_settings, screen, doges, doge_number, row_number):
    """Create a doge and place it in the row"""
    doge = Doge(ai_settings, screen)
    doge_width = doge.rect.width
    # Spacing between each doge is equal to one doge width.
    doge.x = doge_width + 2 * doge_width * doge_number
    doge.rect.x = doge.x
    doge.rect.y = doge.rect.height + 2 * doge.rect.height * row_number
    doges.add(doge)

def create_fleet(ai_settings, screen, ship, doges):
    """Create a full fleet of doges."""
    # Create an doge and find the number of doges in a row.
    doge = Doge(ai_settings, screen)
    number_doges_x = get_number_doges_x(ai_settings, doge.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
        doge.rect.height)

    # Create the fleet of doges
    for row_number in range(number_rows):
        for doge_number in range(number_doges_x):
            create_doge(ai_settings, screen, doges, doge_number, row_number)

def check_fleet_edges(ai_settings, doges):
    """Respond appropriately if any doges have reached an edge."""
    for doge in doges.sprites():
        if doge.check_edges():
            change_fleet_direction(ai_settings, doges)
            break

def change_fleet_direction(ai_settings, doges):
    """Drop the entire fleet and change the fleet's direction."""
    for doge in doges.sprites():
        doge.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, doges, bullets):
    """Respond to ship being hit by doge."""

    if stats.ships_left > 1:
        # Decrement ships_left
        stats.ships_left -= 1

        # Update scoreboard
        sb.prep_ships()

        # Empty the list of doges and bullets.
        doges.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, doges)
        ship.center_ship()

        # Pause
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_doges_bottom(ai_settings, screen, stats, sb, ship, doges, bullets):
    """Check if any doges have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for doge in doges.sprites():
        if doge.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, doges, bullets)
            break

def update_doges(ai_settings, screen, stats, sb, ship, doges, bullets):
    """
    Check if the fleet is at an edge,
    and then update the postions of all doges in the fleet.
    """
    check_fleet_edges(ai_settings, doges)
    doges.update()

    # Look for doge-ship collisions
    if pygame.sprite.spritecollideany(ship, doges):
        ship_hit(ai_settings, screen, stats, sb, ship, doges, bullets)

    # Look for doges hitting the bottom of the screen.
    check_doges_bottom(ai_settings, screen, stats, sb, ship, doges, bullets)

def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()