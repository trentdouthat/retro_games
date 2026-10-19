import pgzrun

WIDTH = 800
HEIGHT = 600

player = Actor('player')
player.pos = (WIDTH // 2, HEIGHT - 80)

# Create an empty list to keep track of all active lasers on screen
lasers = []

def draw():
    screen.clear()
    player.draw()
    
    # Draw every active laser
    for laser in lasers:
        laser.draw()

def update():
    speed = 5
    
    # Player Movement
    if keyboard.left and player.left > 0:
        player.x -= speed
    if keyboard.right and player.right < WIDTH:
        player.x += speed
        
    # Move lasers upward and remove them if they leave the screen
    for laser in lasers[:]:  # Iterate over a copy to safely remove items
        laser.y -= 10
        if laser.bottom < 0:
            lasers.remove(laser)

# This built-in Pygame Zero function fires automatically on a single key press
def on_key_down(key):
    if key == keys.SPACE:
        # Spawn a new laser at the tip of the player's ship
        new_laser = Actor('laser')
        new_laser.pos = player.pos
        lasers.append(new_laser)

pgzrun.go()