import pgzrun

# Set window dimensions
WIDTH = 800
HEIGHT = 600

# Create the Player Actor using the 'player.png' we generated
# (Do not include the extension or 'images/' path in the string)
player = Actor('player')
player.pos = (WIDTH // 2, HEIGHT - 80)

def draw():
    screen.clear()
    # Draw the player sprite onto the screen
    player.draw()

def update():
    # Movement speed
    speed = 5
    
    # Handle keyboard input
    if keyboard.left and player.left > 0:
        player.x -= speed
    if keyboard.right and player.right < WIDTH:
        player.x += speed
    if keyboard.up and player.top > 0:
        player.y -= speed
    if keyboard.down and player.bottom < HEIGHT:
        player.y += speed

pgzrun.go()