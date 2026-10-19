import pgzrun
import random

WIDTH = 800
HEIGHT = 600

explosions = []

def draw():
    screen.clear()
    for particle in explosions:
        screen.draw.filled_circle((particle['x'], particle['y']), particle['size'], particle['color'])

def update():
    # Loop backward to safely remove dead particles
    for particle in explosions[:]:
        particle['x'] += particle['vx']
        particle['y'] += particle['vy']
        particle['life'] -= 1
        if particle['life'] % 5 == 0 and particle['size'] > 1:
            particle['size'] -= 1
        if particle['life'] <= 0:
            explosions.remove(particle)

    # AUTO-SPAWN SWITCH: If the screen is empty, drop a new firework!
    if not explosions:
        # Pick a random origin anywhere on the playfield
        spawn_x = random.randint(100, WIDTH - 100)
        spawn_y = random.randint(100, HEIGHT - 100)
        
        # Pick a dominant random color profile for this specific blast
        theme_color = random.choice([
            (255, 50, 50),   # Neon Red
            (50, 255, 50),   # Neon Green
            (50, 100, 255),  # Deep Blue
            (255, 255, 50),  # Bright Yellow
            (255, 50, 255)   # Purple Fusion
        ])
        
        # Pack the list with 50 high-velocity particle dictionaries
        for _ in range(50):
            explosions.append({
                'x': spawn_x, 'y': spawn_y,
                'vx': random.uniform(-6, 6), 'vy': random.uniform(-6, 6),
                'size': random.randint(3, 6),
                'color': theme_color,
                'life': random.randint(20, 50)
            })

pgzrun.go()