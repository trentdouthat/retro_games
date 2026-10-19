# Lunar Lander Game

# --- 1. Environment bootstrap (Must run before Pygame/pgzrun loads) ---
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

# --- 2. Standard library imports ---
import math
import typing
from typing import Final

# --- 3. Third-party runtime imports ---
import pgzrun
from pgzero.actor import Actor
from pgzero.builtins import keyboard

# --- 4. Static type hints (Ignored at runtime, used only by VS Code / Pylance) ---
if typing.TYPE_CHECKING:
    from pgzero.screen import Screen
    screen: Screen
    keys: typing.Any

# --- 5. Game Configurations & Constants ---
WIDTH = 800
HEIGHT = 700

# Physics Constants
GRAVITY = 0.035          # Downward acceleration per frame
THRUST_POWER = 0.09      # Engine acceleration per frame
ROTATION_SPEED = 2.5     # Degrees per frame
SAFE_LAND_SPEED = 1.2    # Maximum safe touchdown velocity

# Game State
lander = Actor('lander', (WIDTH // 2, 80), anchor=('center', 'bottom'))
vx = 0.0                 # Horizontal velocity
vy = 0.0                 # Vertical velocity
fuel = 1000.0            # Fuel units
thrusting = False
landed = False
crashed = False

def update():
    global vx, vy, fuel, thrusting, landed, crashed

    if landed or crashed:
        return

    # 1. Rotation Controls
    if keyboard.left:
        lander.angle += ROTATION_SPEED
    if keyboard.right:
        lander.angle -= ROTATION_SPEED

    # 2. Main Thruster (Up Arrow)
    thrusting = False
    if keyboard.up and fuel > 0:
        thrusting = True
        fuel -= 1.5

        # Pygame Zero angle 0 is facing right, but Actor images typically face up.
        # If your sprite faces UP at angle 0:
        rad = math.radians(lander.angle)
        # Trigonometric thrust components
        vx -= THRUST_POWER * math.sin(rad)
        vy -= THRUST_POWER * math.cos(rad)

    # 3. Apply Environment Physics
    vy += GRAVITY        # Constant gravity pull
    lander.x += vx       # Apply horizontal inertia
    lander.y += vy       # Apply vertical inertia

    # Screen Wrap (Horizontal)
    if lander.x < 0:
        lander.x = WIDTH
    elif lander.x > WIDTH:
        lander.x = 0

    # 4. Floor Check (Basic ground touchdown)
    ground_y = HEIGHT - 60
    if lander.y >= ground_y:
        lander.y = ground_y
        # Evaluate touchdown constraints
        speed = math.sqrt(vx**2 + vy**2)
        tilt = abs(lander.angle % 360)

        # Allow slight tilt tolerance (near 0 or 360)
        is_upright = tilt <= 10 or tilt >= 350

        if speed <= SAFE_LAND_SPEED and is_upright:
            landed = True
        else:
            crashed = True
        vx = 0
        vy = 0

def draw():
    screen.clear()

    # Draw Ground
    screen.draw.line((0, HEIGHT - 50), (WIDTH, HEIGHT - 50), color="white")

    # Draw Lander
    lander.draw()

    # Optional: Draw simple vector flame when thrusting
    if thrusting:
        rad = math.radians(lander.angle)
        flame_x = lander.x + 20 * math.sin(rad)
        flame_y = lander.y + 20 * math.cos(rad)
        screen.draw.filled_circle((flame_x, flame_y), 4, (255, 120, 30))

    # Instrument Panel (HUD)
    speed = math.sqrt(vx**2 + vy**2)
    speed_color = "green" if speed <= SAFE_LAND_SPEED else "red"

    screen.draw.text(f"ALTITUDE: {max(0, int(HEIGHT - 60 - lander.y))}", (20, 20), color="white", fontsize=22)
    screen.draw.text(f"SPEED: {speed:.2f}", (20, 50), color=speed_color, fontsize=22)
    screen.draw.text(f"FUEL: {int(fuel)}", (WIDTH - 150, 20), color="yellow" if fuel > 200 else "red", fontsize=22)

    # End State Displays
    if landed:
        screen.draw.text("SUCCESSFUL TOUCHDOWN!", center=(WIDTH // 2, HEIGHT // 3), color="green", fontsize=42)
        screen.draw.text("Press 'R' to Launch Again", center=(WIDTH // 2, HEIGHT // 3 + 50), color="white", fontsize=24)
    elif crashed:
        screen.draw.text("CRITICAL IMPACT - DESTROYED", center=(WIDTH // 2, HEIGHT // 3), color="red", fontsize=42)
        screen.draw.text("Press 'R' to Try Again", center=(WIDTH // 2, HEIGHT // 3 + 50), color="white", fontsize=24)

def reset_lander():
    global vx, vy, fuel, thrusting, landed, crashed
    lander.pos = (WIDTH // 2, 80)
    lander.angle = 0
    vx = 0.0
    vy = 0.0
    fuel = 1000.0
    thrusting = False
    landed = False
    crashed = False

def on_key_down(key):
    if key == keys.R and (landed or crashed):
        reset_lander()

pgzrun.go()