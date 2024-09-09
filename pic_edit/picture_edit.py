from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

from config import root_path


def create_weather():
    d_font = ImageFont.truetype(font=f"{root_path}/pic_edit/SecondaSoftIt.woff", size=300)
    e_font = ImageFont.truetype(font=f"{root_path}/pic_edit/RFDewi-Black.ttf", size=110)
    f_font = ImageFont.truetype(font=f"{root_path}/pic_edit/RFDewi-Regular.ttf", size=110)
    pogoda = Image.open(f"{root_path}/pic_edit/1.jpg")
    pogoda_ = pogoda.crop((30, 270, 600, 650))
    resized = pogoda_.resize((1500, 1200))
    ex = Image.open(f"{root_path}/pic_edit/ex.jpg")
    ex.paste(resized, (25, 475))
    drawer = ImageDraw.Draw(ex)
    weekdays = {
        0: 'Пн',
        1: 'Вт',
        2: 'Ср',
        3: 'Чт',
        4: 'Пт',
        5: 'Сб',
        6: 'Вс',
    }
    months = {
        1: 'Янв',
        2: 'Фев',
        3: 'Мар',
        4: 'Апр',
        5: 'Май',
        6: 'Июн',
        7: 'Июл',
        8: 'Авг',
        9: 'Сен',
        10: 'Окт',
        11: 'Ноя',
        12: 'Дек',
    }
    drawer.text((78, 175), str(datetime.now().date().day), font=d_font, fill='white')
    drawer.text((50, 35), str(weekdays.get(datetime.now().date().weekday())), font=e_font, fill='Red')
    drawer.text((218, 35), str(months.get(datetime.now().month)), font=f_font, fill='Grey')
    ex.save(f"{root_path}/pic_edit/2.jpg")
    return True
