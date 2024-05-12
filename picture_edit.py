from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

d_font = ImageFont.truetype("arial.ttf", 300)

pogoda = Image.open("1.jpg")
pogoda_ = pogoda.crop((0, 256, 588, 767))
resized = pogoda_.resize((1500, 1200))
ex = Image.open("ex.jpg")
ex.paste(resized, (25, 470))
drawer = ImageDraw.Draw(ex)
drawer.text((50, 145), str(datetime.now().date().day), font=d_font, fill='white')

ex.show()
