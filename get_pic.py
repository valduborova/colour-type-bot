from PIL import Image, ImageDraw, ImageFont

def get_colors(colors):
    img = Image.new('RGB', (400, 150), color=(255, 255, 255))

    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    draw.text((10, 10), "Your colours:", fill=(0, 0, 0), font=font)

    x = 10
    y = 50

    for label, color in colors.items():

        draw.ellipse((x, y, x+50, y+50), fill=color, outline=(0, 0, 0))
        draw.text((x, y+60), label, fill=(0, 0, 0), font=font)
        x += 100

    img.save('your_colours.png')

    print("Image created!")
    return 'your_colours.png'
