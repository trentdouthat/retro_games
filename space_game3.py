#####################################
# Space Game - Part 3: Alien Fire!
# By: Trent Douthat
# https://www.youtube.com/watch?v=ZyQjKqL8s9
#####################################

import pgzrun
import random
import typing
from pgzero.actor import Actor
from pgzero.builtins import keyboard # 'screen' removed from here since it's not used in this file, 
                                           # but it is used in the draw() function below, so it will be 
                                           # imported implicitly by pgzrun when it runs the game.


# This block only runs inside your editor's brain; Python ignores it at runtime!
import typing
if typing.TYPE_CHECKING:
    from pgzero.screen import Screen
    screen: Screen
    keys: typing.Any

# Configurations
game_state = "PLAY"  # Can be "PLAY", "GAME_OVER", or "VICTORY"
WIDTH = 800
HEIGHT = 600
ENEMY_WIDTH = 64
ENEMY_HEIGHT = 64
ENEMY_COLS = 5
ENEMY_ROWS = 2

player = Actor('player')
player.pos = (WIDTH // 2, HEIGHT - 80)
lives = 3

lasers = []
enemy_lasers = []
enemies = []
explosions = []

enemy_speed = 2
enemy_drop = 20

# Symmetric Grid Spawning
padding_x = 40
padding_y = 30
total_fleet_width = (ENEMY_COLS * ENEMY_WIDTH) + ((ENEMY_COLS - 1) * padding_x)
# (5 * 64) + ((5 - 1) * 40) = 320 + 160 = 480 pixels total fleet footprint
start_x = (WIDTH // 2) - (total_fleet_width // 2) + (ENEMY_WIDTH // 2) 
# (800 // 2) - (480 // 2) + (64 // 2) = 400 - 240 + 32 = 192

for enemy_row in range(ENEMY_ROWS):
    for enemy_col in range(ENEMY_COLS):
        enemy = Actor('enemy')
        enemy.x = start_x + (enemy_col  * (ENEMY_WIDTH + padding_x))
        enemy.y = 100 + (enemy_row * (ENEMY_HEIGHT + padding_y))
        enemies.append(enemy)

def draw():
    screen.clear()

    if game_state == "PLAY":
        player.draw()
        for laser in lasers: laser.draw()
        for e_laser in enemy_lasers: e_laser.draw()
        for enemy in enemies: enemy.draw()
        for particle in explosions:
            screen.draw.filled_circle((particle['x'], particle['y']), particle['size'], particle['color'])
            screen.draw.text(f"LIVES: {lives}", (20, 20), color="white", fontsize=30)

    elif game_state == "GAME_OVER":
        # Massive red text in the center of the screen
        screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2), color="red", fontsize=80)
        screen.draw.text("The alien fleet has prevailed.", center=(WIDTH // 2, (HEIGHT // 2) + 60), color="white", fontsize=30)
        screen.draw.text("Press 'R' to Restart", center=(WIDTH // 2, HEIGHT - 50), color="gray", fontsize=25)

    elif game_state == "VICTORY":
        # Draw the fireworks celebration
        for particle in explosions:
            screen.draw.filled_circle((particle['x'], particle['y']), particle['size'], particle['color'])
            screen.draw.text("You have saved the sector!", center=(WIDTH // 2, (HEIGHT // 2) + 40), color="green", fontsize=30)
            screen.draw.text("Press 'R' to Restart", center=(WIDTH // 2, HEIGHT - 50), color="gray", fontsize=25)

def update():
    global enemy_speed, lives, game_state
    
    # If player is out of lives, stop updating the game
    if game_state == "GAME_OVER":
        return
    
    if game_state == "VICTORY":
        # Keep updating the fireworks celebration
        for particle in explosions[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            if particle['life'] % 5 == 0 and particle['size'] > 1:
                particle['size'] -= 1
            if particle['life'] <= 0:
                explosions.remove(particle)
    
        if not explosions:
            spawn_x = random.randint(100, WIDTH - 100)
            spawn_y = random.randint(100, HEIGHT - 100)
            theme_color = random.choice([(255, 50, 50), (50, 255, 50), (255, 255, 50)])
            for _ in range(30):
                explosions.append({
                    'x': spawn_x, 'y': spawn_y,
                    'vx': random.uniform(-5, 5), 'vy': random.uniform(-5, 5),
                    'size': random.randint(2, 5),
                    'color': theme_color,
                    'life': random.randint(20, 40)
                })
            return

    # Check for Lose Conditions
    if lives <= 0:
        game_state = "GAME_OVER"
        return
        
    # Check if any alien reached the bottom floor
    for enemy in enemies:
        if enemy.bottom >= player.top:
            game_state = "GAME_OVER"
            return

    # Check for Win Condition (Dynamic Truthiness!)
    if not enemies:
        game_state = "VICTORY"
        return

    speed = 5

    # 1. Player Movement
    if keyboard.left and player.left > 0: player.x -= speed
    if keyboard.right and player.right < WIDTH: player.x += speed

    # 2. Update Player Lasers
    for laser in lasers[:]:
        laser.y -= 10
        if laser.bottom < 0: lasers.remove(laser)
    
    # 3. Enemy Fleet Marching
    move_down = False
    for enemy in enemies:
        enemy.x += enemy_speed
        if enemy.right >= WIDTH or enemy.left <= 0:
            move_down = True

    if move_down:
        enemy_speed = -enemy_speed
        for enemy in enemies:
            enemy.y += enemy_drop

    # 4. Random Alien Firing Logic
    # If there are enemies alive, roll a 100-sided die every frame
    if enemies and random.randint(1, 100) == 1:
        # Pick one random enemy from the list
        shooter = random.choice(enemies)
        new_e_laser = Actor('laser') # Using the same template as the player's laser sprite!
        new_e_laser.pos = shooter.pos
        enemy_lasers.append(new_e_laser)

    # 5. Move Enemy Lasers Downward
    for e_laser in enemy_lasers[:]:
        e_laser.y += 7 # Moves DOWN instead of up
        if e_laser.top > HEIGHT:
            enemy_lasers.remove(e_laser)
        # Check if enemy laser hits the player
        elif e_laser.colliderect(player):
            lives -= 1
            enemy_lasers.remove(e_laser)
            # This is where we will trigger an explosion event in the future, but for now we will just remove the laser and decrement lives.

    # 6. Player Laser vs. Enemy Collision
    for laser in lasers[:]:
        for enemy in enemies[:]:
            if laser.colliderect(enemy):
                for _ in range(20):
                    explosions.append({
                        'x': enemy.x, 'y': enemy.y,
                        'vx': random.uniform(-4, 4), 'vy': random.uniform(-4, 4),
                        'size': random.randint(2, 5),
                        'color': random.choice([(50, 255, 50), (255, 255, 0), (255, 100, 0)]),
                        'life': random.randint(15, 30)
                    })
                if laser in lasers: lasers.remove(laser)
                if enemy in enemies: enemies.remove(enemy)

    # 7. Particle Physics
    for particle in explosions[:]:
        particle['x'] += particle['vx']
        particle['y'] += particle['vy']
        particle['life'] -= 1
        if particle['life'] % 5 == 0 and particle['size'] > 1: particle['size'] -= 1
        if particle['life'] <= 0: explosions.remove(particle)

def on_key_down(key):
    if key == keys.SPACE and lives > 0:
        new_laser = Actor('laser')
        new_laser.pos = player.pos
        lasers.append(new_laser)

    if key == keys.R and game_state != "PLAY":
        reset_game()


def reset_game():
    global lives, game_state, enemy_speed, lasers, enemy_lasers, enemies, explosions
    
    lives = 3
    game_state = "PLAY"
    enemy_speed = 2
    
    # Clear out old active projectiles or explosion remnants
    lasers.clear()
    enemy_lasers.clear()
    explosions.clear()
    enemies.clear()
    
    # Repopulate the full symmetric alien fleet grid
    for row in range(ENEMY_ROWS):
        for col in range(ENEMY_COLS):
            enemy = Actor('enemy')
            enemy.x = start_x + (col * (ENEMY_WIDTH + padding_x))
            enemy.y = 100 + (row * (ENEMY_HEIGHT + padding_y))
            enemies.append(enemy)
            
    # Reset player position to the bottom center mark
    player.pos = (WIDTH // 2, HEIGHT - 80)

pgzrun.go()

        
