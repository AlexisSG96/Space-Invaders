"""
Name: Alexis Steven Garcia
Project: Space Invaders
Date: October 8, 2018
Email: AlexisSG96@csu.fullerton.edu
"""
import sys
import pygame
import random
from bullet import Bullet
from laser import Laser
from alien import Alien
from ufo import Ufo
from time import sleep


def check_keydown_events(event, ai_settings, screen, game_active, ship, bullets):
    """Check if key is pressed."""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            ship.moving_left = True
        elif event.key == pygame.K_SPACE and game_active:
            fire_bullet(ai_settings, screen, ship, bullets)
        elif event.key == pygame.K_q:
            sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fires a bullet if available."""
    # Create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        ship.ship_bullet_sound()
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """Check if keys are no longer pressed."""
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, lasers, bullets):
    """Check key presses as events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stats.save_high_score()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats.game_active, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, lasers, bullets, mouse_x,
                              mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, lasers, bullets, mouse_x, mouse_y):
    """Check if play button has been pressed."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)
        
        # Reset the game statistics
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ship()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        lasers.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, play_button, bunkers, ufo):
    """Update the screen with all objects as needed."""
    # Check if ufo should come out
    if stats.game_active:
        check_ufo_event(ai_settings, screen, ufo)

    # Redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets in front of ship
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Redraw all lasers under aliens
    for laser in lasers.sprites():
        laser.blitme()

    # Draw the score information
    sb.show_score()

    # Redraw a ufo if needed
    if ufo:
        ufo.update()
        for ufos in ufo.sprites():
            ufos.blitme()

    # Draw aliens and ship
    ship.blitme()
    aliens.draw(screen)

    # Draw bunker as needed
    check_bunker_collisions(lasers, bullets, bunkers)
    bunkers.update()

    # Draw play button if not active
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible
    pygame.display.flip()


def check_high_score(stats, sb):
    """Check if high score needs to be updated."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo):
    """Update ship bullets as needed."""
    # Update bullet positions
    bullets.update()

    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo)


def update_lasers(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo):
    """Update alien lasers as needed."""
    lasers.update()
    for laser in lasers.copy():
        if laser.rect.bottom > ai_settings.screen_height:
            lasers.remove(laser)
    check_laser_ship_collisions(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo):
    """Check if bullet collides with alien or ufo."""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False, collided=alien_collision_check)
    if collisions:
        for aliens in collisions.values():
            for alien in aliens:
                stats.score += ai_settings.alien_points[str(alien.alien_type)]
                alien.begin_death()
            sb.prep_score()
        check_high_score(stats, sb)

    ufo_collision = pygame.sprite.groupcollide(bullets, ufo, True, False, collided=alien_collision_check)
    if ufo_collision:
        for ufos in ufo:
            stats.score = stats.score + ufos.score
            ufos.begin_death()
        sb.prep_high_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        if ufo:
            for ufos in ufo.sprites():
                ufos.kill()
        # If the entire fleet is destroyed, start a new level
        bullets.empty()
        lasers.empty()
        ai_settings.increase_speed()
        # Increase level
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def alien_collision_check(bullet, alien):
    """Return whether alien should be dead."""
    if alien.dead:
        return False
    return pygame.sprite.collide_rect(bullet, alien)


def check_laser_ship_collisions(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo):
    """Check that any alien lasers have collided with the ship."""
    collide = pygame.sprite.spritecollideany(ship, lasers) 
    if collide: 
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo)


def check_bunker_collisions(lasers, bullets, bunkers):
    """Check if bullet or laser hits a bunker."""
    pygame.sprite.groupcollide(bullets, bunkers, True, True)
    pygame.sprite.groupcollide(lasers, bunkers, True, True)


def get_number_aliens_x(ai_settings, alien_width):
    """Get the number of aliens that fill a fleet."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Get the space available for aliens."""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create aliens depending on what row they are in."""
    if row_number < 2:
        alien_type = 1
    elif row_number < 4:
        alien_type = 2
    else:
        alien_type = 3
    alien = Alien(ai_settings, screen, alien_type)
    alien_width = alien.rect.width
    alien.x = alien_width + 1.25 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1.25 * alien.rect.height * row_number
    alien.rect.y += int(ai_settings.screen_height / 8)
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create the fleet using different aliens."""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # Create the fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def create_random_ufo(ai_settings, screen):
    """Create a random ufo to go across the screen."""
    ufo = None
    time_stamp = None
    if random.randrange(0, 100) <= 10:  # 10% chance of ufo
        ufo = Ufo(ai_settings, screen)
        time_stamp = pygame.time.get_ticks()
    return time_stamp, ufo


def check_ufo_event(ai_settings, screen, ufo_group):
    """Check if ufo has been gone for long."""
    if not ai_settings.time_from_last_ufo and not ufo_group:
        ai_settings.time_from_last_ufo, n_ufo = create_random_ufo(ai_settings, screen)
        if n_ufo:
            ufo_group.add(n_ufo)
    elif abs(pygame.time.get_ticks() - ai_settings.time_from_last_ufo) > ai_settings.ufo_interval and not ufo_group:
        ai_settings.time_from_last_ufo, n_ufo = create_random_ufo(ai_settings, screen)
        if n_ufo:
            ufo_group.add(n_ufo)


def check_fleet_edges(ai_settings, aliens):
    """Check if fleet hits edges of screen."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Change direction of fleet."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, ufo):
    """Ship has been hit so initialize ship settings as needed."""
    # Kill ufo if on screen.
    if ufo:
        for ufos in ufo.sprites():
            ufos.kill()
    ship.ship_death()
    ship.update()
    while ship.dead:
        screen.fill(ai_settings.bg_color)
        ship.blitme()
        pygame.display.flip()
        ship.update()
    if stats.ships_left > 0:
        # Decrement ships_left
        stats.ships_left -= 1

        # Update scoreboard
        sb.prep_ship()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        lasers.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)

    # Game over, so play sound and save high score if needed.
    else:
        pygame.mixer.music.load('sounds/game_end.wav')
        pygame.mixer.music.play()
        stats.game_active = False
        stats.save_high_score()
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo):
    """Check if aliens reach bottom."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo)
            break


def fire_laser(ai_settings, screen, aliens, lasers):
    """Random laser fired from random alien."""
    alien_fired = random.choice(aliens.sprites())
    if len(lasers) < ai_settings.lasers_allowed and (ai_settings.laser_stamp is None
                                                     or (abs(pygame.time.get_ticks() - ai_settings.laser_stamp) >
                                                         ai_settings.laser_time)):
        new_laser = Laser(ai_settings, screen, alien_fired)
        alien_fired.invader_shoot()
        lasers.add(new_laser)


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo):
    """Update aliens as needed."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo)
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo)
    if aliens.sprites():
        fire_laser(ai_settings, screen, aliens, lasers)
