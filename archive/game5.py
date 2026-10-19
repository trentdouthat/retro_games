import pgzrun

WIDTH = 800
HEIGHT = 600

# Setup Player
player = Actor('player')
player.pos = (WIDTH // 2, HEIGHT - 80)

# Lists to track active game elements
lasers = []
enemies = []

# Spawn a row of 5 enemies across the top of the screen at startup
for i in range(5):
    enemy = Actor('enemy')
    enemy.x = 120 + (i * 140)  # Space them out evenly
    enemy.y = 80
    enemies.append(enemy)

def draw():
    screen.clear()
    player.draw()
    
    for laser in lasers:
        laser.draw()
        
    for enemy in enemies:
        enemy.draw()

def update():
    speed = 5
    
    # 1. Player Movement
    if keyboard.left and player.left > 0:
        player.x -= speed
    if keyboard.right and player.right < WIDTH:
        player.x += speed
        
    # 2. Update Lasers (using our copy trick to safely remove!)
    for laser in lasers[:]:
        laser.y -= 10
        if laser.bottom < 0:
            lasers.remove(laser)
            
    # 3. Collision Detection (The "Shooting Something" Logic)
    # We check every active laser against every active enemy
    for laser in lasers[:]:
        for enemy in enemies[:]:
            # colliderect checks if the rectangular boundaries of the two actors overlap
            if laser.colliderect(enemy):
                # If they hit, delete both from their original lists!
                if laser in lasers: 
                    lasers.remove(laser)
                if enemy in enemies:
                    enemies.remove(enemy)

def on_key_down(key):
    if key == keys.SPACE:
        new_laser = Actor('laser')
        new_laser.pos = player.pos
        lasers.append(new_laser)

pgzrun.go()