from PIL import Image

# Create a 64x64 alien enemy sprite
enemy_img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
e_pixels = enemy_img.load()

# Deep alien green and bright neon green accents
colors_enemy = {
    "G": (0, 150, 0, 255),    # Main Body
    "N": (50, 255, 50, 255),  # Neon Highlights
    "Y": (255, 255, 0, 255),  # Glowing Eyes
}

enemy_map = [
    "....GG......GG....",
    "....GG......GG....",
    ".....GG....GG.....",
    "......GGGGGG......",
    "....GGNYGGYNGG....",
    "....GGNYGGYNGG....",
    "  GGGGGGGGGGGGGG  ",
    "  GGGGGGGGGGGGGG  ",
    "GGGGNNGGGGGGNNGGGG",
    "GGGGNNGGGGGGNNGGGG",
    "GG..GGGGGGGGGG..GG",
    "....GG..GG..GG....",
    "....GG..GG..GG....",
    "....  ..  ..  ....",
]

# Note: This map is 18 cols wide, so let's map it into our 64x64 space
for row_idx, row in enumerate(enemy_map):
    for col_idx, char in enumerate(row):
        if char in colors_enemy:
            for y_offset in range(3): # Slightly smaller multiplier to fit
                for x_offset in range(3):
                    pixel_x = col_idx * 3 + x_offset + 5
                    pixel_y = row_idx * 3 + y_offset + 5
                    e_pixels[pixel_x, pixel_y] = colors_enemy[char]

enemy_img.save("images/enemy.png", "PNG")
print("Enemy sprite created!")