from PIL import Image, ImageDraw

# Create a blank white image
img = Image.new("RGB", (400, 300), color="white")

# Get a drawing context
draw = ImageDraw.Draw(img)

# Draw shapes
draw.rectangle((50, 50, 350, 250), outline="blue", width=5)
draw.ellipse((150, 100, 250, 200), fill="red")

# Add some text
draw.text((60, 20), "Hello, Pillow!", fill="black")

# Save the image
img.save("simple_image.png")

# Show it
img.show()