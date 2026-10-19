import pgzrun
import random

WIDTH = 800
HEIGHT = 600

player = Actor('player')
player.pos = (WIDTH // 2, HEIGHT - 80)

lasers = []
enemies = []
explosions = []

for i in range(5):
    enemy = Actor('enemy')
    enemy.x = 120 + (i * 140)
    enemy.y = 80
    enemies.append(enemy)

def draw():
    screen.clear()
    player.draw()
    for laser in lasers: laser.draw()
    for enemy in enemies: enemy.draw()
    for particle in explosions:
        screen.draw.filled_circle((particle['x'], particle['y']), particle['size'], particle['color'])

def update():
    speed = 5
    if keyboard.left and player.left > 0: player.x -= speed
    if keyboard.right and player.right < WIDTH: player.x += speed
        
    for laser in lasers[:]:
        laser.y -= 10
        if laser.bottom < 0: lasers.remove(laser)
            
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
