import pgzrun
from pgzero.actor import Actor
import random

WIDTH = 800
HEIGHT = 600

player = Actor('player')
player.pos = (WIDTH // 2, HEIGHT - 80)

lasers = []
enemies = []
explosions = []

# --- NEW STATE VARIABLES ---
enemy_speed = 2      # Positive means moving right, negative means left
enemy_drop = 20      # How far down they shift when hitting a wall

# ---------------------------

# Spawn a grid of enemies (2 rows, 5 columns) with calculated spacing

# Game Configurations
ENEMY_WIDTH = 64
ENEMY_HEIGHT = 64
COLS = 5
ROWS = 2

# Let's space them out by adding a small gap (padding) between them
padding_x = 40
padding_y = 30

# The fleet has 5 columns, meaning there are 4 gaps of padding between them
total_fleet_width = (COLS * ENEMY_WIDTH) + ((COLS - 1) * padding_x)
# (5 * 64) + (4 * 40) = 320 + 160 = 480 pixels total fleet footprint

# Now find the true start_x for the first enemy's CENTER
# Center of the screen minus half of the fleet footprint
start_x = (WIDTH // 2) - (total_fleet_width // 2) + (ENEMY_WIDTH // 2)
# 400 - 240 + 32 = 192

for row in range(ROWS):
    for col in range(COLS):
        enemy = Actor('enemy')
        
        # Mathematically calculate X and Y relative to screen boundaries
        enemy.x = start_x + (col * (ENEMY_WIDTH + padding_x))
        enemy.y = 100 + (row * (ENEMY_HEIGHT + padding_y)) # 100px down from the top ceiling
        
        enemies.append(enemy)

#***************************


#*********************************
def draw():
    screen.clear()
    player.draw()
    for laser in lasers: laser.draw()
    for enemy in enemies: enemy.draw()
    for particle in explosions:
        screen.draw.filled_circle((particle['x'], particle['y']), particle['size'], particle['color'])

def update():
    # Bring our movement variables into the function scope
    global enemy_speed
    
    speed = 5
    
    # 1. Player Movement
    if keyboard.left and player.left > 0: player.x -= speed
    if keyboard.right and player.right < WIDTH: player.x += speed
        
    # 2. Update Lasers
    for laser in lasers[:]:
        laser.y -= 10
        if laser.bottom < 0: lasers.remove(laser)
            
    # 3. NEW: Enemy Movement & Wall Bumping
    move_down = False
    
    # Check if ANY enemy is about to hit the left or right edge
    for enemy in enemies:
        enemy.x += enemy_speed
        if enemy.right >= WIDTH or enemy.left <= 0:
            move_down = True

    # If an edge was hit, reverse direction and shift everyone down
    if move_down:
        enemy_speed = -enemy_speed  # Reverse direction (positive becomes negative, vice versa)
        for enemy in enemies:
            enemy.y += enemy_drop
                    
    # 4. Collision Detection
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
                    
    # 5. Particle Physics
    for particle in explosions[:]:
        particle['x'] += particle['vx']
        particle['y'] += particle['vy']
        particle['life'] -= 1
        if particle['life'] % 5 == 0 and particle['size'] > 1: particle['size'] -= 1
        if particle['life'] <= 0: explosions.remove(particle)

def on_key_down(key):
    if key == keys.SPACE:
        new_laser = Actor('laser')
        new_laser.pos = player.pos
        lasers.append(new_laser)

pgzrun.go()