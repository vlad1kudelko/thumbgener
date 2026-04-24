import random

from PIL import Image, ImageDraw, ImageFilter

from src.thumbgener.Thumbgener import Thumbgener


class ThumbgenerBlob(Thumbgener):
    def __init__(self):
        self.count_ellipse = 20

    def draw(self, title, filename) -> None:
        # 1. рисуем холст
        bg_color = tuple(random.randint(230, 255) for _ in range(3))
        image = Image.new("RGBA", (self.width, self.height), bg_color)
        draw = ImageDraw.Draw(image)

        # 2. рисуем капли
        for _ in range(self.count_ellipse):
            color = tuple(random.randint(100, 255) for _ in range(3))
            blob_size = random.randint(100, 300)  # диаметр окружности
            half_size = blob_size // 2  # т.к. рисуем от левого верхнего угла окружности
            x = random.randint(-half_size, self.width - half_size)
            y = random.randint(-half_size, self.height - half_size)
            draw.ellipse([x, y, x + blob_size, y + blob_size], fill=color)

        # 3. рисуем размытие
        image = image.filter(ImageFilter.GaussianBlur(radius=15))
        draw = ImageDraw.Draw(image)

        # 4. рисуем текст
        self.draw_text(title, draw)

        # 5. сохраняем в файл
        image = image.convert("RGB")  # убираем альфа-канал
        image.convert("RGB").save(filename)
