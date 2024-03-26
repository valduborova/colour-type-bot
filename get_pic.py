from PIL import Image, ImageDraw, ImageFont

def get_colors(colors):
    # Create a new blank image
    img = Image.new('RGB', (400, 150), color=(255, 255, 255))

    # Initialize ImageDraw to draw on the image
    draw = ImageDraw.Draw(img)

    # Load a font
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    # Draw the "Your colors:" text
    draw.text((10, 10), "Your colours:", fill=(0, 0, 0), font=font)

    # Starting positions for the first circle and text
    x = 10
    y = 50

    # Draw each circle and its label
    for label, color in colors.items():
        # Draw circle
        draw.ellipse((x, y, x+50, y+50), fill=color, outline=(0, 0, 0))

        # Draw label
        draw.text((x, y+60), label, fill=(0, 0, 0), font=font)

        # Move to the right for the next circle and label
        x += 100

    # Save the image
    img.save('your_colours.png')

    print("Image created!")
    return 'your_colours.png'
