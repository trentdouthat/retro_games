import pgzrun

WIDTH = 800
HEIGHT = 600

# Create a 50x50 pixel rectangle box acting as your character
# pos = (x, y, width, height)
player = Rect((375, 500, 50, 50))

def draw():
    screen.clear()
    screen.fill((30, 20, 50)) # Dark purple background
    
    # Draw your character box on the screen in bright cyan blue
    screen.draw.filled_rect(player, (0, 200, 255))

def update():
    # Move the box using arrow keys
    if keyboard.left and player.left > 0:
        player.x -= 5
    if keyboard.right and player.right < WIDTH:
        player.x += 5
    if keyboard.up and player.top > 0:
        player.y -= 5
    if keyboard.down and player.bottom < HEIGHT:
        player.y += 5

pgzrun.go()