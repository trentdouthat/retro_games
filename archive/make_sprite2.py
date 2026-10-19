from PIL import Image

# Create a small 16x16 laser sprite
laser_img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
l_pixels = laser_img.load()

# Draw a simple vertical energy beam line down the center
for y in range(4, 12):
    for x in range(7, 9):
        l_pixels[x, y] = (255, 0, 0, 255) # Bright Red

laser_img.save("images/laser.png", "PNG")