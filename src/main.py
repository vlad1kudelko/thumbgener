import random
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


def thumbgen(title, filename):
    width, height = 800, 400
    bg_color = (
        random.randint(230, 255),
        random.randint(230, 255),
        random.randint(230, 255),
    )
    image = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(image)

    for _ in range(20):
        r = random.randint(100, 255)
        g = random.randint(100, 255)
        b = random.randint(100, 255)
        alpha = random.randint(50, 150)
        color = (r, g, b, alpha)

        blob_size = random.randint(100, 300)
        x = random.randint(-50, width)
        y = random.randint(-50, height)

        draw.ellipse([x, y, x + blob_size, y + blob_size], fill=color)

    image = image.filter(ImageFilter.GaussianBlur(radius=15))
    draw = ImageDraw.Draw(image)

    font_size = 50
    dirname = Path(__file__).parent
    font = ImageFont.truetype(dirname / "fonts" / "Ubuntu-Medium.ttf", font_size)

    # Автоматический перенос: width=25 — это примерное кол-во символов в строке
    wrapper = textwrap.TextWrapper(width=20)
    lines = wrapper.wrap(text=title)

    # Вычисляем общую высоту текстового блока
    line_padding = 10
    line_heights = [draw.textbbox((0, 0), line, font=font)[3] for line in lines]
    total_text_height = sum(line_heights) + line_padding * (len(lines) - 1)

    # Рисуем каждую строку
    current_y = (height - total_text_height) // 2
    for line in lines:
        # Центрируем каждую строку по горизонтали
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        line_x = (width - line_width) // 2

        draw.text((line_x, current_y), line, font=font, fill=(40, 40, 40))

        current_y += line_heights[0] + line_padding

    image = image.convert("RGB")  # Убираем альфа-канал для сохранения в JPG/PNG
    image.convert("RGB").save(filename)
