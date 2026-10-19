from PIL import Image

# Create a 64x64 image with a transparent background (RGBA: Red, Green, Blue, Alpha)
img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
pixels = img.load()

# Define the classic sci-fi retro spaceship using coordinate blocks
# Using a deep red/orange palette with bright engine glows
colors = {
    "H": (200, 0, 0, 255),    # Hull (Red)
    "A": (255, 69, 0, 255),   # Accents (Orange)
    "W": (0, 255, 255, 255),  # Windshield / Cockpit (Cyan)
    "E": (255, 215, 0, 255),  # Engine Glow (Gold)
}

# 16x16 matrix mapped onto a 64x64 grid (each block is 4x4 pixels)
sprite_map = [
    "....HHHHHHHH....",
    "....HHHHHHHH....",
    ".....WWWWWW.....",
    ".....WWWWWW.....",
    "....HHHHHHHH....",
    "....HHHHHHHH....",
    "...HHAHHHHHAH...",
    "...HHAHHHHHAH...",
    "..HHAAHHHHAAHH..",
    "..HHAAHHHHAAHH..",
    ".HHHAAHHHHAAHHH.",
    ".HHHAAHHHHAAHHH.",
    "HHHHHHHHHHHHHHHH",
    "HHHHHHHHHHHHHHHH",
    ".EE..........EE.",
    ".EE..........EE."
]

# Scale up and draw the pixels
for row_idx, row in enumerate(sprite_map):
    for col_idx, char in enumerate(row):
        if char in colors:
            # Draw a 4x4 block for that retro chunky pixel look
            for y_offset in range(4):
                for x_offset in range(4):
                    pixel_x = col_idx * 4 + x_offset
                    pixel_y = row_idx * 4 + y_offset
                    pixels[pixel_x, pixel_y] = colors[char]

# Save directly to your project directory
# Pygame Zero looks for images in an 'images' folder
import os
os.makedirs("images", exist_ok=True)
img.save("images/player.png", "PNG")
print("Sprite successfully created at images/player.png!")