import pgzrun

# 1. Set window dimensions
WIDTH = 800
HEIGHT = 600

# 2. Create your knight character (looks for 'hero.png' inside your images folder)
player = Actor('hero')
player.pos = (400, 500) # Start near the bottom center

def draw():
    screen.clear()
    screen.fill((30, 20, 50)) # Dark purple background
    player.draw()

def update():
    # 3. Move the character using keyboard arrow keys
    if keyboard.left and player.left > 0:
        player.x -= 5
    if keyboard.right and player.right < WIDTH:
        player.x += 5
    if keyboard.up and player.top > 0:
        player.y -= 5
    if keyboard.down and player.bottom < HEIGHT:
        player.y += 5

# 4. Start the engine
pgzrun.go()
