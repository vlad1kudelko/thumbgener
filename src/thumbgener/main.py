import random
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


class Thumbgener:
    def __init__(self):
        self.width = 800
        self.height = 400
        self.count_ellipse = 20
        self.font_size = 50
        self.font_file = "Ubuntu-Medium.ttf"
        self.font_margin = 50

    def draw(self, title, filename):
        bg_color = tuple(random.randint(230, 255) for _ in range(3))
        image = Image.new("RGBA", (self.width, self.height), bg_color)
        draw = ImageDraw.Draw(image)

        for _ in range(self.count_ellipse):
            color = (
                *[random.randint(100, 255) for _ in range(3)],
                random.randint(50, 150),
            )
            blob_size = random.randint(100, 300)  # диаметр окружности
            half_size = blob_size // 2  # т.к. рисуем от левого верхнего угла окружности
            x = random.randint(-half_size, self.width - half_size)
            y = random.randint(-half_size, self.height - half_size)
            draw.ellipse([x, y, x + blob_size, y + blob_size], fill=color)

        image = image.filter(ImageFilter.GaussianBlur(radius=15))
        draw = ImageDraw.Draw(image)

        dirname = Path(__file__).parent
        font = ImageFont.truetype(dirname / "fonts" / self.font_file, self.font_size)

        max_width = self.width - (self.font_margin * 2)
        # Автоматический перенос: width=25 — это примерное кол-во символов в строке
        wrapper = textwrap.TextWrapper(width=20)
        lines = wrapper.wrap(text=title)

        # Вычисляем общую высоту текстового блока
        line_padding = 10
        line_heights = [draw.textbbox((0, 0), line, font=font)[3] for line in lines]
        total_text_height = sum(line_heights) + line_padding * (len(lines) - 1)

        # Рисуем каждую строку
        current_y = (self.height - total_text_height) // 2
        for line in lines:
            # Центрируем каждую строку по горизонтали
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]
            line_x = (self.width - line_width) // 2
            draw.text((line_x, current_y), line, font=font, fill=(40, 40, 40))
            current_y += line_heights[0] + line_padding

        image = image.convert("RGB")  # Убираем альфа-канал для сохранения в JPG/PNG
        image.convert("RGB").save(filename)
