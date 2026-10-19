import pgzrun
import random

WIDTH = 800
HEIGHT = 600

# Setup Player & Lists
player = Actor('player')
player.pos = (WIDTH // 2, HEIGHT - 80)

lasers = []
enemies = []
explosions = []  # Holds active particle groups

# Spawn enemies
for i in range(5):
    enemy = Actor('enemy')
    enemy.x = 120 + (i * 140)
    enemy.y = 80
    enemies.append(enemy)

def draw():
    screen.clear()
    player.draw()
    
    for laser in lasers:
        laser.draw()
        
    for enemy in enemies:
        enemy.draw()
        
    # Draw individual explosion particles
    # screen.draw.filled_circle takes (center_x, center_y), radius, and (R, G, B)
    for particle in explosions:
        screen.draw.filled_circle(
            (particle['x'], particle['y']), 
            particle['size'], 
            particle['color']
        )

def update():
    speed = 5
    
    # 1. Player Movement
    if keyboard.left and player.left > 0:
        player.x -= speed
    if keyboard.right and player.right < WIDTH:
        player.x += speed
        
    # 2. Update Lasers
    for laser in lasers[:]:
        laser.y -= 10
        if laser.bottom < 0:
            lasers.remove(laser)
            
    # 3. Collision & Spawning Particles
    for laser in lasers[:]:
        for enemy in enemies[:]:
            if laser.colliderect(enemy):
                
                # --- NEW: Spawn 20 particle dictionaries right at the enemy's center
                for _ in range(20):
                    p = {
                        'x': enemy.x,
                        'y': enemy.y,
                        # Random velocity vectors (moves them out in all directions)
                        'vx': random.uniform(-4, 4),
                        'vy': random.uniform(-4, 4),
                        # Random sizes and bright neon green/yellow explosion colors
                        'size': random.randint(2, 5),
                        'color': random.choice([(50, 255, 50), (255, 255, 0), (255, 100, 0)]),
                        'life': random.randint(15, 30)  # How many frames the particle lasts
                    }
                    explosions.append(p)
                # --- End Particle Spawn
                
                if laser in lasers: lasers.remove(laser)
                if enemy in enemies: enemies.remove(enemy)
                    
    # 4. Animate Particle Physics (using our trusty copy trick again!)
    for particle in explosions[:]:
        particle['x'] += particle['vx']
        particle['y'] += particle['vy']
        particle['life'] -= 1  # Standard countdown clock
        
        # Shrink the particle slightly as it burns out
        if particle['life'] % 5 == 0 and particle['size'] > 1:
            particle['size'] -= 1
            
        # Remove dead particles so we don't lag the engine
        if particle['life'] <= 0:
            explosions.remove(particle)

def on_key_down(key):
    if key == keys.SPACE:
        new_laser = Actor('laser')
        new_laser.pos = player.pos
        lasers.append(new_laser)

pgzrun.go()